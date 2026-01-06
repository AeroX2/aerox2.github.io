#version 300 es
precision highp float;

#define MAX_STEPS 160
#define MAX_DEPTH 160.0
#define MIN_DIST (1.0 / 16384.0)

#define BASE_TEXTURE 0.0
#define FONT_TEXTURE 1.0
#define SIDE_FONT_TEXTURE 2.0

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

  vec4 t = textureLod(iTexture, uv, 0.0);
  vec3 msd = t.rgb;
  float sd = t.w - 0.5;

  return sd;
}

float rand(vec2 co) {
  return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

vec2 sdfScene(vec3 p) {
  vec3 s = vec3(1.4, 1.5, 1.0);
  vec3 q = p;

  // Slow drift downwards
  q.y += iTime * 0.5;

  vec3 q2 = round(q / s);
  if (q2.z < 0.0) q2.z = 0.0;
  q = q - s * q2;

  // "DNA Twist" / Vortex effect
  // Rotate around the Y axis based on height (q2.y is the grid row) + time
  float twist = q2.y * 0.2 + iTime * 0.5;
  q.xz *= rot2D(twist);

  // Gentle tumble on individual elements
  q.xy *= rot2D(sin(iTime + q2.y) * 0.5);
  q.yz *= rot2D(cos(iTime * 0.8) * 0.5);

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

float calcSoftShadow(vec3 ro, vec3 rd, float mint, float maxt, float k) {
  float res = 1.0;
  float t = mint;
  for (int i = 0; i < 50; i++) {
    if (t >= maxt) break;
    float h = sdfScene(ro + rd * t).x;
    if (h < 0.001) return 0.0;
    res = min(res, k * h / t);
    t += h;
  }
  return res;
}

float calcAO(vec3 pos, vec3 nor) {
  float occ = 0.0;
  float sca = 1.0;
  for (int i = 0; i < 5; i++) {
    float h = 0.001 + 0.15 * float(i) / 4.0;
    float d = sdfScene(pos + h * nor).x;
    occ += (h - d) * sca;
    sca *= 0.95;
  }
  return clamp(1.0 - 1.5 * occ, 0.0, 1.0);
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

    // normalU = normalU+0.000000001;
    normal = normalize(normalU);
  }

  return vec2(t, i);
}

mat3 setCamera(vec3 ro, vec3 ta, float cr) {
  vec3 cw = normalize(ta - ro);
  vec3 cp = vec3(sin(cr), cos(cr), 0.0);
  vec3 cu = normalize(cross(cw, cp));
  vec3 cv = normalize(cross(cu, cw));
  return mat3(cu, cv, cw);
}

void main() {
  vec2 uv = v_uv;
  vec2 m = iMouse;

  // Target moves in a circle ("Eyes following edge of a circle")
  vec3 ta = vec3(sin(iTime * 0.5), cos(iTime * 0.5), 0.0);

  // Camera Position controlled by mouse (Original style)
  vec3 ro = vec3(0.0, 0.0, -3.5);
  ro.yz *= rot2D(-m.y * 2.0 + 0.5); // Add slight offset to center view vertically
  ro.xz *= rot2D(-m.x * 4.0);

  // Camera-to-World transformation
  mat3 ca = setCamera(ro, ta, 0.0);

  // Ray direction
  vec3 rd = ca * normalize(vec3((uv - 0.5) * 2.5, 2.0));

  vec3 normal = vec3(0.0);
  float mat = 0.0;
  vec2 r = rayMarch(ro, rd, normal, mat);

  vec3 color;
  if (r.x <= MAX_DEPTH) {
    vec3 p = ro + rd * r.x;
    vec3 texColor = vec3(0.1, 0.125, 0.1) * 0.5;

    // Lighting
    vec3 lig = normalize(vec3(0.0, 0.0, -2.0));
    float dif = clamp(dot(normal, lig), 0.0, 1.0);
    float sh = calcSoftShadow(p, lig, 0.02, 2.5, 8.0);
    float ao = calcAO(p, normal);

    vec3 lightColor = dif * sh * vec3(1.2) + vec3(0.9) * ao;

    if (mat == FONT_TEXTURE) {
      texColor = vec3(0.3, 0.3, 0.9);
    }

    color = texColor * lightColor;
    // color = normal * 0.5 + 0.5;
  } else {
    color = vec3(0.0);
  }

  fragColor = vec4(color, 1.0);
}
