"""Small procedural-texture toolkit (numpy + PIL). Everything it makes tiles seamlessly."""
import os, json
import numpy as np
from PIL import Image

N = 1024


def _freq(n=N):
    f = np.fft.fftfreq(n) * n
    return np.meshgrid(f, f, indexing="xy")


def norm01(a):
    a = a - a.min()
    return a / (a.max() + 1e-9)


def fnoise(seed, beta=1.6, lo=1.0, hi=None, sx=1.0, sy=1.0, n=N):
    """Periodic fractal noise. beta = spectral slope, lo/hi = band limits in cycles per tile,
    sx/sy > 1 stretch the features along that axis (streaks)."""
    rng = np.random.default_rng(seed)
    fx, fy = _freq(n)
    r = np.sqrt((fx * sx) ** 2 + (fy * sy) ** 2)
    amp = np.where(r > 0, 1.0 / np.maximum(r, 1e-6) ** beta, 0.0)
    amp = amp * (r >= lo)
    if hi is not None:
        amp = amp * np.exp(-(r / hi) ** 4)
    spec = amp * np.exp(2j * np.pi * rng.random((n, n)))
    return norm01(np.real(np.fft.ifft2(spec)))


def blur(a, radius):
    """Periodic gaussian blur."""
    fx, fy = _freq(a.shape[0])
    g = np.exp(-2 * (np.pi * radius / a.shape[0]) ** 2 * (fx ** 2 + fy ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(a) * g))


def grid(n=N):
    u = (np.arange(n) + 0.5) / n
    return np.meshgrid(u, u, indexing="xy")      # U (x, 0..1), V (y, 0..1)


def lerp(a, b, t):
    return a + (b - a) * t


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0 + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


def color(c, t=None):
    """Return an HxWx3 colour field. c is an rgb tuple; t optionally scales brightness."""
    out = np.ones((N, N, 3)) * np.array(c)[None, None, :]
    return out if t is None else out * t[..., None]


def mix(c0, c1, t):
    return color(c0) * (1 - t[..., None]) + color(c1) * t[..., None]


def normal_map(h, strength):
    """Tangent-space normal map from a height field (periodic central differences). Unreal convention (green down)."""
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5 * strength * h.shape[0] / 100.0
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5 * strength * h.shape[0] / 100.0
    nz = np.ones_like(h)
    l = np.sqrt(dx * dx + dy * dy + nz * nz)
    return np.stack([-dx / l * 0.5 + 0.5, dy / l * 0.5 + 0.5, nz / l * 0.5 + 0.5], -1)


def to_srgb(lin):
    lin = np.clip(lin, 0, 1)
    return np.where(lin <= 0.0031308, lin * 12.92, 1.055 * np.power(lin, 1 / 2.4) - 0.055)


class Writer:
    def __init__(self, out_dir):
        self.out = out_dir
        os.makedirs(out_dir, exist_ok=True)
        self.manifest = {}

    def save(self, name, base_color, height, rough, size_cm, bump=1.0, metallic=0.0):
        """base_color: linear rgb HxWx3. height 0..1. rough 0..1 (scalar or field). size_cm: real size of one tile."""
        bc = (to_srgb(base_color) * 255 + 0.5).astype(np.uint8)
        Image.fromarray(bc, "RGB").save(os.path.join(self.out, "T_%s_BC.png" % name))
        nm = (np.clip(normal_map(height, bump), 0, 1) * 255 + 0.5).astype(np.uint8)
        Image.fromarray(nm, "RGB").save(os.path.join(self.out, "T_%s_N.png" % name))
        r = np.clip(rough * np.ones((N, N)), 0, 1)
        orh = np.stack([r, np.ones((N, N)), np.clip(height, 0, 1)], -1)          # R = roughness, G = spare, B = height
        Image.fromarray((orh * 255 + 0.5).astype(np.uint8), "RGB").save(os.path.join(self.out, "T_%s_R.png" % name))
        self.manifest[name] = {"size_cm": size_cm, "metallic": metallic}

    def finish(self):
        with open(os.path.join(self.out, "manifest.json"), "w") as f:
            json.dump(self.manifest, f, indent=1)
