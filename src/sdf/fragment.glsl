#version 300 es
precision highp float;

#define MAX_STEPS 100
#define MIN_DIST 0.01

uniform float iTime;
uniform vec2 iResolution;
uniform vec2 iMouse;
uniform sampler2D iTexture;
in vec2 v_uv;
out vec4 fragColor;

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

float opSmoothUnion( float d1, float d2, float k )
{
    float h = clamp( 0.5 + 0.5*(d2-d1)/k, 0.0, 1.0 );
    return mix( d2, d1, h ) - k*h*(1.0-h);
}

float opSmoothSubtraction( float d1, float d2, float k )
{
    float h = clamp( 0.5 - 0.5*(d2+d1)/k, 0.0, 1.0 );
    return mix( d2, -d1, h ) + k*h*(1.0-h);
}

float opSmoothIntersection( float d1, float d2, float k )
{
    float h = clamp( 0.5 - 0.5*(d2-d1)/k, 0.0, 1.0 );
    return mix( d2, d1, h ) + k*h*(1.0-h);
}

float smoothAbs(float z, float epsilon) {
    return 0.5 * (z + sqrt(z * z + epsilon * epsilon));
}

float sdSphere(vec3 p, float s) {
    return length(p) - s;
}

float sdBox(vec3 p, vec3 radius)
{
  vec3 dist = abs(p) - radius;
  return min(max(dist.x, max(dist.y, dist.z)), 0.0) + length(max(dist, 0.0));
}

float sdPlane( vec3 p, vec3 n, float h )
{
  // n must be normalized
  return dot(p,n) + h;
}

float sdFont(vec2 p) {
    vec2 uv = (p * 0.5 + 0.5);
    
    vec4 t = texture(iTexture, uv * vec2(1., 1.), -1000.0);
    vec3 msd = t.rgb;
    float sd = t.w - 0.5;// + 1./1000.;
    
    // float value = (dot(vec2(0.2), 0.5*fwidth(uv)))*(sd - 0.5);
    // float value = sd; // (dot(vec2(0.2), 0.5*fwidth(uv)))*(sd - 0.5);
    // float smoothValue = clamp(value + 0.5, 0.0, 1.0);
    return sd;
}

float sdf(vec3 p) {
    // float plane = dot(p,vec3(0.,0.,1.)) + 4.;

    vec3 s = vec3(1.4,1.5,1.);

    vec3 spherePos = p - vec3(sin(iTime*2.) * 2.0, 0, 0);
    
    float sphere = sdSphere(spherePos, 1.0);
    

    vec3 q2 = (p - s*round(p/s));
    vec3 q = (p - s*clamp(round(p/s), -vec3(1000.,1000.,0.), vec3(1000.,1000.,1000.)));
    // q.xz *= rot2D(iTime);
    
    float fontSdf = sdFont(p.xy) - 0.01;

    float box = sdBox(p, vec3(.8, 1.2, 2.));
    fontSdf = max(box, fontSdf);
    
    //return sphere2d;
    // return min(sphere, fontSdf);
    float ground = sdPlane(p, vec3(0,.3,0), 1.5);
    ground = min(ground, sdPlane(p, vec3(0,0,-1.), 11.));

    return min(ground, fontSdf);
}

vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.0, 0.33, 0.67);
    
    return a + b*cos(6.28318*(c*t+d));
}

vec2 rayMarch(vec3 ro, vec3 rd) {
    float totalDist = 0.001;
    
    int i;
    for (i = 0; i < MAX_STEPS; i++) {
        vec3 p = ro + rd * totalDist;
        float dist = sdf(p);
        totalDist += dist;
        
        if (abs(dist) < MIN_DIST) {
            break;
        }
        
        if (totalDist > float(MAX_STEPS)) {
            break;
        }
    }
    
    return vec2(totalDist, i);
}

float map(vec3 p) {
	vec3 n = vec3(0, 1, 0);
	float k1 = 1.9;
	float k2 = (sin(p.x * k1) + sin(p.z * k1)) * 0.8;
	float k3 = (sin(p.y * k1) + sin(p.z * k1)) * 0.8;
	float w1 = 4.0 - dot(abs(p), normalize(n)) + k2;
	float w2 = 4.0 - dot(abs(p), normalize(n.yzx)) + k3;
	float s1 = length(mod(p.xy + vec2(sin((p.z + p.x) * 2.0) * 0.3, cos((p.z + p.x) * 1.0) * 0.5), 2.0) - 1.0) - 0.2;
	float s2 = length(mod(0.5+p.yz + vec2(sin((p.z + p.x) * 2.0) * 0.3, cos((p.z + p.x) * 1.0) * 0.3), 2.0) - 1.0) - 0.2;
	return min(w1, min(w2, min(s1, s2)));
}

void main() {
    vec2 uv = v_uv;
    vec2 m = iMouse;

    vec3 ro = vec3(0.0, 0.0, -3.0);
    vec3 rd = normalize(vec3((uv - 0.5) * 2.5, 1.0));

    ro.yz *= rot2D(-m.y);
    rd.yz *= rot2D(-m.y);

    ro.xz *= rot2D(-m.x);
    rd.xz *= rot2D(-m.x);

    vec2 r = rayMarch(ro, rd);

    float t = r.x;
    vec3 ip = ro + rd * t;
	vec3 col = vec3(t * 0.01);
	col = sqrt(col);
	fragColor = vec4(0.05*t+abs(rd) * col + max(0.0, map(ip - 0.1) - t), 1.0); //Thanks! Shane!
   
    // vec3 color = vec3(r.y) / 80.;
    // fragColor = vec4(color, 1.0);
}
