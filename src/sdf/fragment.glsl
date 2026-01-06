#version 300 es
precision highp float;

#define MAX_STEPS 160
#define MAX_DEPTH 100.0
#define MIN_DIST (1.0 / 10000.0)

#define BASE_TEXTURE 0.0
#define FONT_TEXTURE 1.0
#define SIDE_FONT_TEXTURE 2.0

uniform float iTime;
uniform vec2 iResolution;
uniform vec2 iMouse;
uniform sampler2D iTexture;
in vec2 v_uv;
out vec4 fragColor;

mat2 rot2D(float angle) {
  float s = sin(angle);
  float c = cos(angle);
  return mat2(c, -s, s, c);
}

float sdBox(vec3 p, vec3 radius) {
  vec3 dist = abs(p) - radius;
  return min(max(dist.x, max(dist.y, dist.z)), 0.0) + length(max(dist, 0.0));
}

float sdBoxWithCone(vec3 p, vec3 b, float cone) {
  float k = clamp(p.y / b.y * 0.5 + 0.5, 0.0, 1.0);
  float s = mix(1.0 - cone, 1.0, k);
  vec3 d = abs(p) - b * vec3(s, 1.0, s);
  return length(max(d, 0.0)) + min(max(d.x, max(d.y, d.z)), 0.0);
}

// Signed distance to an isosceles triangle prism aligned to XY axis
// h.x = half-width, h.y = height
float sdTriPrism(vec3 p, vec2 h, float thick) {
  p.y = -p.y;
  vec2 q = vec2(h.x, 2.0 * h.y);
  vec2 p2 = p.xy;
  p2.x = abs(p2.x);
  p2.y += h.y; 
  
  vec2 a = p2 - q * clamp(dot(p2, q) / dot(q, q), 0.0, 1.0);
  vec2 b = p2 - q * vec2(clamp(p2.x / q.x, 0.0, 1.0), 1.0);
  float d2d = sqrt(min(dot(a, a), dot(b, b)));
  if (max(p2.x * q.y - p2.y * q.x, p2.y - q.y) < 0.0) d2d = -d2d;
  
  float dZ = abs(p.z) - thick;
  return length(max(vec2(d2d, dZ), 0.0)) + min(max(d2d, dZ), 0.0);
}

float sdLeg(vec3 p) {
  p = vec3(p.x, -p.y, p.z + 0.074522); 

  // Precomputed mat2 for rot2D(-0.698132) - 4A
  const mat2 rotA = mat2(0.76604, 0.64279, -0.64279, 0.76604);
  // Precomputed mat2 for rot2D(0.872664) - 4B
  const mat2 rotB = mat2(0.64279, -0.76604, 0.76604, 0.64279);
  // Precomputed mat2 for rot2D(2.96706) - 4C
  const mat2 rotC = mat2(-0.98481, -0.17365, 0.17365, -0.98481);

  vec3 pA = p - vec3(-0.790497, 0.369614, 0.0);
  pA.xy *= rotA; 
  float dA = sdTriPrism(pA, vec2(0.06, 0.32), 0.03);

  vec3 pB = p - vec3(-0.860115, 0.649188, 0.0);
  pB.xy *= rotB; 
  float dB = sdTriPrism(pB, vec2(0.04, 0.14), 0.03);

  vec3 pC = p - vec3(-0.55827, -0.130416, 0.0);
  pC.xy *= rotC; 
  float dC = sdTriPrism(pC, vec2(0.06, 0.32), 0.03);

  return min(min(dA, dB), dC);
}

float sdHead(vec3 p) {
  // Shape 3A (Add)
  vec3 pA = p - vec3(0, 1.56052, 0);
  pA.yz = -pA.yz; // Manual PI rotation
  float dA = sdBoxWithCone(pA, vec3(1.35, 0.63, 0.08) * 0.5, 1.0);

  // Shape 3B (Sub) - Mirror Z
  vec3 pB = p;
  pB.z = abs(pB.z);
  pB -= vec3(0, -1.55428, 0.032445);
  pB.yz = -pB.yz; 
  float dB = sdBoxWithCone(pB, vec3(0.72, 0.64, 0.02) * 0.5, 1.0);

  return max(-dB, dA);
}

float sdBoat(vec3 q) {
  const mat2 rot45 = mat2(0.70711, -0.70711, 0.70711, 0.70711);

  // --- Group 1 (Main Body) ---
  vec3 p1a = q;
  p1a.xz *= rot45;
  float d1a = sdBoxWithCone(p1a, vec3(2.0, 1.0, 2.0) * 0.5, 1.0);

  vec3 q1_sym = q;
  q1_sym.z = abs(q1_sym.z);
  vec3 p1b = q1_sym - vec3(0.023976, 0.003795, 1.075014);
  p1b.yz *= rot2D(-0.300197);
  float d1b = sdBox(p1b, vec3(3.0, 2.0, 2.0) * 0.5 - 0.1) - 0.1;

  float d1 = max(-d1b, d1a);

  // --- Group 2 (Inner Shell Subtraction) ---
  vec3 q2 = (q - vec3(0, 0.148846, 0)) / 1.14;
  vec3 p2a = q2;
  p2a.xz *= rot45;
  float d2a = sdBoxWithCone(p2a, vec3(2.0, 1.0, 2.0) * 0.5, 1.0);

  vec3 q2_sym = q2;
  q2_sym.z = abs(q2_sym.z);
  vec3 p2b = q2_sym - vec3(0.023976, 0.003795, 1.075014);
  p2b.yz *= rot2D(-0.300197);
  float d2b = sdBox(p2b, vec3(3.0, 2.0, 2.0) * 0.5 - 0.1) - 0.1;

  float d2 = max(-d2b, d2a) * 1.14;

  // --- Final Combination ---
  float d = max(-d2, d1);

  // --- Group 3 (Head) ---
  d = min(d, sdHead(q - vec3(0.0, -1.06269, 0.0)));

  // --- Legs ---
  d = min(d, sdLeg(q - vec3(0.0, -0.05623, -0.04952))); // BR
  d = min(d, sdLeg(q - vec3(1.08709, -0.12884, 0.19098))); // FL

  vec3 qFR = q - vec3(0.80479, 0.54173, 0.038);
  qFR.xy *= rot2D(-1.13446); qFR.xz *= rot2D(-0.12217);
  d = min(d, sdLeg(qFR));

  vec3 qBL = q - vec3(-0.24313, 0.4717, 0.16557);
  qBL.xy *= rot2D(-0.87266); 
  d = min(d, sdLeg(qBL));

  return d;
}

vec2 sdfScene(vec3 p) {
  vec3 q = p;
  float t = iTime;

  // 1. Twist Animation (Y-axis)
  float kT = sin(t * 1.2) * 0.4;
  float ct = cos(kT * q.y);
  float st = sin(kT * q.y);
  q.xz *= mat2(ct, -st, st, ct);

  // 2. Cheap Bend Animation (X-axis)
  float kB = cos(t * 1.5) * 0.2;
  float cb = cos(kB * q.x);
  float sb = sin(kB * q.x);
  q.xy *= mat2(cb, -sb, sb, cb);

  float d = sdBoat(q);
  return vec2(d, 1.0);
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
  for (int i = 0; i < 24; i++) {
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
    if (abs(dist) < MIN_DIST || t > MAX_DEPTH) break;
  }

  if (t < MAX_DEPTH) {
    vec3 smallVec = vec3(1.0 / 4096.0, 0, 0);
    vec3 normalU = vec3(
        sdfScene(p + smallVec.xyy).x - sdfScene(p - smallVec.xyy).x,
        sdfScene(p + smallVec.yxy).x - sdfScene(p - smallVec.yxy).x,
        sdfScene(p + smallVec.yyx).x - sdfScene(p - smallVec.yyx).x
    );
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
  vec3 ta = vec3(0.0, 0.0, 0.0);
  vec3 ro = vec3(0.0, 0.0, -2.2);
  ro.yz *= rot2D(-m.y * 2.0 + 0.5);
  ro.xz *= rot2D(-m.x * 4.0);
  mat3 ca = setCamera(ro, ta, 0.0);
  vec2 p = uv - 0.5;
  p.x *= iResolution.x / iResolution.y;
  vec3 rd = ca * normalize(vec3(p * 2.5, 2.0));

  vec3 normal = vec3(0.0);
  float mat = 0.0;
  vec2 r = rayMarch(ro, rd, normal, mat);

  vec3 color;
  if (r.x <= MAX_DEPTH) {
    vec3 p = ro + rd * r.x;
    vec3 texColor = vec3(0.05, 0.06, 0.05);

    vec3 lig = normalize(vec3(1.0, 1.0, -2.0));
    float dif = clamp(dot(normal, lig), 0.0, 1.0);
    float sh = calcSoftShadow(p, lig, 0.02, 2.5, 8.0);
    float ao = calcAO(p, normal);

    vec3 lightColor = dif * sh * vec3(1.2) + vec3(0.15) * ao;
    if (mat == FONT_TEXTURE) texColor = vec3(0.3, 0.3, 0.9);
    color = texColor * lightColor;
  } else {
    color = vec3(0.0);
  }
  fragColor = vec4(color, 1.0);
}
