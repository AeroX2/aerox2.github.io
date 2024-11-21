import vertexShaderSource from './vertex.glsl?raw';
import fragmentShaderSource from './fragment.glsl?raw';

export class WebGL {
  private gl: WebGL2RenderingContext | null;

  private mousePos: { x: number; y: number } = { x: 0, y: 0 };
  private fontTexture: WebGLTexture | null;

  private iTimeLocation: WebGLUniformLocation | null;
  private iResolutionLocation: WebGLUniformLocation | null;
  private iMouseLocation: WebGLUniformLocation | null;

  constructor(private canvas: HTMLCanvasElement) {
    this.gl = canvas.getContext('webgl2');

    this.iTimeLocation = null;
    this.iResolutionLocation = null;
    this.iMouseLocation = null;
    this.fontTexture = null;
  }

  compileShader(source: string, type: number) {
    if (this.gl == null) return;

    const gl = this.gl;
    const shader = gl.createShader(type);
    if (shader == null) return;

    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.error('Error compiling shader: ', gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  }

  createProgram(vertexSource: string, fragmentSource: string) {
    if (this.gl == null) return;

    const gl = this.gl;
    const vertexShader = this.compileShader(vertexSource, gl.VERTEX_SHADER);
    const fragmentShader = this.compileShader(
      fragmentSource,
      gl.FRAGMENT_SHADER
    );
    if (vertexShader == null || fragmentShader == null) return;

    const program = gl.createProgram();
    if (program == null) return;

    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      console.error('Error linking program: ', gl.getProgramInfoLog(program));
      return null;
    }

    return program;
  }

  init() {
    if (this.gl == null) return;

    const gl = this.gl;
    const program = this.createProgram(
      vertexShaderSource,
      fragmentShaderSource
    );
    if (program == null) return;
    gl.useProgram(program);

    this.iTimeLocation = gl.getUniformLocation(program, 'iTime');
    this.iResolutionLocation = gl.getUniformLocation(program, 'iResolution');
    this.iMouseLocation = gl.getUniformLocation(program, 'iMouse');

    gl.uniform2f(
      this.iResolutionLocation,
      this.canvas.width,
      this.canvas.height
    );

    const vertices = new Float32Array([
      -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0
    ]);
    const vertexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

    const positionLocation = gl.getAttribLocation(program, 'iScreenPosition');
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLocation);

    const iTextureLocation = gl.getUniformLocation(program, 'iTexture');
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, this.fontTexture);
    gl.uniform1i(iTextureLocation, 0);
  }

  loop() {
    if (this.gl == null) return;

    const gl = this.gl;
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.uniform1f(this.iTimeLocation, performance.now() / 1000);
    gl.uniform2f(this.iMouseLocation, this.mousePos.x, this.mousePos.y);

    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, this.fontTexture);

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }

  loadFontTexture(image: HTMLImageElement) {
    if (this.gl == null) return;

    const gl = this.gl;
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);

    const placeholder = new Uint8Array([255, 0, 0, 255]);
    gl.texImage2D(
      gl.TEXTURE_2D,
      0,
      gl.RGBA,
      1,
      1,
      0,
      gl.RGBA,
      gl.UNSIGNED_BYTE,
      placeholder
    );

    image.onload = function () {
      gl.bindTexture(gl.TEXTURE_2D, texture);
      gl.texImage2D(
        gl.TEXTURE_2D,
        0,
        gl.RGBA,
        gl.RGBA,
        gl.UNSIGNED_BYTE,
        image
      );

      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);

      gl.bindTexture(gl.TEXTURE_2D, null);
    };

    this.fontTexture = texture;
  }

  setMousePos(mousePos: { x: number; y: number }) {
    this.mousePos = mousePos;
  }

  resetViewport() {
    if (this.gl == null) return;

    const aspectRatio = 16 / 9;
    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = rect.width;
    this.canvas.height = rect.width / aspectRatio;

    this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
  }

  isSupported() {
    return this.gl != null;
  }
}
