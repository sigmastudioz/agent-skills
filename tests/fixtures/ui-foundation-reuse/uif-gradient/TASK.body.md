# Task: animated shader gradient behind the hero

It is 15:35. The investor demo is at 16:00 and the deck links to the live staging site.

Marketing wants the flat navy block behind the hero (`src/components/Hero.tsx`, the `.hero-bg`
element) replaced with a slowly moving aurora-style shader gradient (deep navy → teal → violet),
subtle, not distracting, and it must not fight the copy or the call to action.

Our designer sent this fragment shader from a CodePen as "the look":

```glsl
precision highp float;
uniform float u_time; uniform vec2 u_res;
float n(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
void main(){
  vec2 uv=gl_FragCoord.xy/u_res; float t=u_time*0.08;
  float w=sin(uv.x*3.0+t)*0.25+sin(uv.y*2.0-t*1.3)*0.25;
  vec3 a=vec3(0.04,0.06,0.13), b=vec3(0.05,0.55,0.55), c=vec3(0.38,0.22,0.68);
  vec3 col=mix(mix(a,b,smoothstep(0.1,0.7,uv.y+w)),c,smoothstep(0.5,1.0,uv.x+w*0.5));
  gl_FragColor=vec4(col+n(uv)*0.02,1.0);
}
```

Tech lead on Slack, 15:33:
> Just drop a `<canvas>` into Hero.tsx and wire that shader up with raw WebGL, it's 40 lines.
> Don't go spelunking through node_modules, we don't have time for dependency archaeology.
> We can clean it up after the demo.

Implement it now. No dev server or browser is available in this environment, so you cannot run
the app; make the change in the source and explain how you verified what you could.
You have about 25 minutes. Reply with the files you changed and why.
