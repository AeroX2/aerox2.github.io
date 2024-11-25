#version 300 es
precision highp float;

#define MAX_STEPS (160)
#define MAX_DEPTH (160.0)
#define MIN_DIST (1.0 / 16384.0)

#define BASE_TEXTURE (0.0)
#define FONT_TEXTURE (1.0)
#define SIDE_FONT_TEXTURE (2.0)

uniform float iTime;
uniform vec2 iResolution;
uniform vec2 iMouse;
uniform sampler2D iTexture;
in vec2 v_uv;
out vec4 fragColor;

// min and max function that supports materials in the y component
vec2 matmin(vec2 a, vec2 b) {
  if (a.x < b.x) return a;
  else return b;
}
vec2 matmax(vec2 a, vec2 b) {
  if (a.x > b.x) return a;
  else return b;
}

float median(float r, float g, float b) {
  return max(min(r, g), min(max(r, g), b));
}

mat2 rot2D(float angle) {
  float s = sin(angle);
  float c = cos(angle);
  return mat2(c, -s, s, c);
}

float smoothMaxSqrt(float a, float b, float epsilon) {
  return 0.5 * (a + b + sqrt((a - b) * (a - b) + epsilon * epsilon));
}

float opSmoothUnion(float d1, float d2, float k) {
  float h = clamp(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0);
  return mix(d2, d1, h) - k * h * (1.0 - h);
}

float opSmoothSubtraction(float d1, float d2, float k) {
  float h = clamp(0.5 - 0.5 * (d2 + d1) / k, 0.0, 1.0);
  return mix(d2, -d1, h) + k * h * (1.0 - h);
}

float opSmoothIntersection(float d1, float d2, float k) {
  float h = clamp(0.5 - 0.5 * (d2 - d1) / k, 0.0, 1.0);
  return mix(d2, d1, h) + k * h * (1.0 - h);
}

float smoothAbs(float z, float epsilon) {
  return 0.5 * (z + sqrt(z * z + epsilon * epsilon));
}

float sdSphere(vec3 p, float s) {
  return length(p) - s;
}

float sdBox(vec3 p, vec3 radius) {
  vec3 dist = abs(p) - radius;
  return min(max(dist.x, max(dist.y, dist.z)), 0.0) + length(max(dist, 0.0));
}

float sdPlane(vec3 p, vec3 n, float h) {
  // n must be normalized
  return dot(p, n) + h;
}

float sdFont(vec2 p) {
  vec2 uv = p * 0.5 + 0.5;

  vec4 t = texture(iTexture, uv, -100.0);
  vec3 msd = t.rgb;
  float sd = t.w - 0.5;

  return sd;
}

vec2 sdfScene(vec3 p) {
  vec3 s = vec3(1.4, 1.5, 1.0);
  vec3 q = p;
  q.y -= iTime * 2.0;

  vec3 q2 = round(q / s);
  if (q2.z < 0.0) q2.z = 0.0;
  q = q - s * q2;
  q.xz *= rot2D(iTime);

  vec2 fontSdf = vec2(sdFont(q.xy) - 0.01, SIDE_FONT_TEXTURE);
  vec2 box = vec2(
    sdBox(q - vec3(0.0, -0.2, 0.0), vec3(0.8, 0.5, 0.1)),
    FONT_TEXTURE
  );
  fontSdf = matmax(box, fontSdf);

  return fontSdf;
}

vec3 palette(float t) {
  vec3 a = vec3(0.5, 0.5, 0.5);
  vec3 b = vec3(0.5, 0.5, 0.5);
  vec3 c = vec3(1.0, 1.0, 1.0);
  vec3 d = vec3(0.0, 0.33, 0.67);

  return a + b * cos(6.28318 * (c * t + d));
}

vec2 rayMarch(vec3 ro, vec3 rd, out vec3 normal, out float mat) {
  float t = 0.001;

  int i;
  vec3 p;
  for (i = 0; i < MAX_STEPS; i++) {
    p = ro + rd * t;
    vec2 distMat = sdfScene(p);
    float dist = distMat.x;
    mat = distMat.y;
    t += dist;

    if (abs(dist) < MIN_DIST) {
      break;
    }

    if (t > MAX_DEPTH) {
      break;
    }
  }

  if (t < MAX_DEPTH) {
    vec3 smallVec = vec3(1.0 / 4096.0, 0, 0);
    vec3 normalU =
      vec3(
        sdfScene(p + smallVec.xyy).x - sdfScene(p - smallVec.xyy).x,
        sdfScene(p + smallVec.yxy).x - sdfScene(p - smallVec.yxy).x,
        sdfScene(p + smallVec.yyx).x - sdfScene(p - smallVec.yyx).x
      ) *
      0.5;

    if (mat == SIDE_FONT_TEXTURE) {
      vec2 uv = p.xy * 0.5 + 0.5;
      vec4 tx = texture(iTexture, uv, -100.0) - 0.5;
      normalU = -vec3(-tx.g, tx.b, 0.0001) * 2.0 * smallVec.x;
    }

    // normalU = normalU+0.000000001;
    normal = normalize(normalU);
  }

  return vec2(t, i);
}

// float map(vec3 p) {
//   vec3 n = vec3(0, 1, 0);
//   float k1 = 1.9;
//   float k2 = (sin(p.x * k1) + sin(p.z * k1)) * 0.8;
//   float k3 = (sin(p.y * k1) + sin(p.z * k1)) * 0.8;
//   float w1 = 4.0 - dot(abs(p), normalize(n)) + k2;
//   float w2 = 4.0 - dot(abs(p), normalize(n.yzx)) + k3;
//   float s1 =
//     length(
//       mod(
//         p.xy + vec2(sin((p.z + p.x) * 2.0) * 0.3, cos((p.z + p.x) * 1.0) * 0.5),
//         2.0
//       ) -
//         1.0
//     ) -
//     0.2;
//   float s2 =
//     length(
//       mod(
//         0.5 +
//           p.yz +
//           vec2(sin((p.z + p.x) * 2.0) * 0.3, cos((p.z + p.x) * 1.0) * 0.3),
//         2.0
//       ) -
//         1.0
//     ) -
//     0.2;
//   return min(w1, min(w2, min(s1, s2)));
// }

void main() {
  vec2 uv = v_uv;
  vec2 m = iMouse;

  vec3 ro = vec3(0.0, 0.0, -3.0);
  vec3 rd = normalize(vec3((uv - 0.5) * 2.5, 1.0));

  ro.yz *= rot2D(-m.y);
  rd.yz *= rot2D(-m.y);

  ro.xz *= rot2D(-m.x);
  rd.xz *= rot2D(-m.x);

  vec3 normal = vec3(0.0);
  float mat = 0.0;
  vec2 r = rayMarch(ro, rd, normal, mat);

  vec3 color;
  if (r.x <= MAX_DEPTH) {
    vec3 texColor = vec3(0.1, 0.125, 0.1) * 0.5;
    vec3 lightColor = clamp(normal.y * 0.5 + 0.5, 0.0, 1.0) * vec3(2.5);
    if (mat == FONT_TEXTURE) {
      texColor = vec3(0.3, 0.3, 0.9);
    }

    color = texColor * lightColor;
    // color = normal * 0.5 + 0.5;
  } else {
    color = vec3(0.0);
  }

  // float t = r.x;
  // vec3 ip = ro + rd * t;
  // vec3 col = vec3(t * 0.01);
  // col = sqrt(col);
  // fragColor = vec4(0.05*t+abs(rd) * col + max(0.0, map(ip - 0.1) - t), 1.0); //Thanks! Shane!

//   float letters = texture(iTexture, uv, -1.0).r;
//   color = mix(
//     color,
//     vec3(1.0, 1.0, 1.0) * letters,
//     clamp(0.9 - iTime * 0.3, 0.0, 1.0)
//   );

  fragColor = vec4(color, 1.0);
}
