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

float sdSphere(vec3 p, float s) {
    return length(p) - s;
}

// float sdBox(vec3 p, vec3 b) {
//     vec3 q = abs(p) - b;
//     return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
// }

float median(float r, float g, float b) {
    return max(min(r, g), min(max(r, g), b));
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

/*float screenPxRange(vec2 uv) {
    vec2 unitRange = vec2(4.)/vec2(16.,16.);
    vec2 screenTexSize = vec2(1.0)/fwidth(uv);
    return max(0.5*dot(unitRange, screenTexSize), 1.0);
}*/

float screenPxRange(vec2 uv) {
    // Assume your MSDF texture resolution (adjust these values as needed)
    const vec2 textureResolution = vec2(8.) / vec2(100.0, 100.0);
    
    // Calculate the screen-space pixel range
    vec2 screenTexSize = textureResolution * fwidth(uv);
    
    // Use an empirically determined scale factor to adjust the smoothing range
    float pxRange = max(0.5 * (screenTexSize.x + screenTexSize.y), 1.0);
    return pxRange;
}

float sdBox(vec3 p, vec3 radius)
{
  vec3 dist = abs(p) - radius;
  return min(max(dist.x, max(dist.y, dist.z)), 0.0) + length(max(dist, 0.0));
}

float sdf2d(vec2 p, float r) {
    vec2 uv = 1. - (p * 0.5 + 0.5);
    
    vec3 msd = texture(iTexture, uv, -100.0).rgb;
    float sd = median(msd.r, msd.g, msd.b);
    
    // float value = (dot(vec2(0.2), 0.5*fwidth(uv)))*(sd - 0.5);
    float value = sd; // (dot(vec2(0.2), 0.5*fwidth(uv)))*(sd - 0.5);
    float smoothValue = clamp(value + 0.5, 0.0, 1.0);
    return 1. - sd;
}

mat2 rot2D(float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return mat2(c, -s, s, c);
}

float opExtrusion(  vec3 p, float h )
{
    float d = sdf2d(p.xy, 0.5);
    vec2 w = vec2( d, abs(p.z) - h );
    return min(max(w.x,w.y),0.0) + length(max(w,0.0));
}

float sdf3d(vec3 p) {
    float plane = dot(p,vec3(0.,0.,1.)) + 4.;

    float ss = 3.;
    vec3 s = vec3(ss,ss,ss);

    vec3 spherePos = p - vec3(sin(iTime) * 3.0, 0, 0);
    
    float sphere = sdSphere(spherePos, 1.0);
    
    vec3 q2 = (p - s*round(p/s));
    vec3 q = (p - s*clamp(round(p/s), -vec3(1000.,1000.,0.), vec3(1000.,1000.,1000.)));
    q.xz *= rot2D(iTime);
    
    float sphere2d = sdf2d(p.xy, 0.5); //opExtrusion(q, 0.1) - 0.01;

    float box = sdBox(p, vec3(1.));
    sphere2d = max(box, sphere2d);
    
    //return sphere2d;
    return min(sphere, sphere2d);
    //return opSmoothUnion(sphere, sphere2d, .4);
}

vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.0, 0.2, 0.3);
    
    return a + b*cos(6.28318*(c*t+d));
}

vec2 rayMarch(vec3 ro, vec3 rd) {
    float totalDist = 0.001;
    
    int i;
    for (i = 0; i < MAX_STEPS; i++) {
        vec3 p = ro + rd * totalDist;
        float dist = sdf3d(p);
        totalDist += dist;
        
        if (abs(dist) < MIN_DIST) {
            return vec2(totalDist, i);
        }
        
        if (totalDist > float(MAX_STEPS)) {
            break;
        }
    }
    
    return vec2(totalDist, i);
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

    vec3 color = palette(r.x * .02 + float(r.y) * 0.01);

    fragColor = vec4(color, 1.0);
}
