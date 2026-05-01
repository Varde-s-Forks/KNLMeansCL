import vapoursynth as vs
import pytest

core = vs.core

if not hasattr(core, "knlm"):
    pytest.skip("KNLMeansCL plugin not loaded", allow_module_level=True)


@pytest.fixture
def gray_clip() -> vs.VideoNode:
    return core.std.BlankClip(format=vs.GRAY8, width=160, height=120, length=10)


@pytest.fixture
def yuv_clip() -> vs.VideoNode:
    return core.std.BlankClip(format=vs.YUV444P8, width=160, height=120, length=10)


@pytest.fixture
def rgb_clip() -> vs.VideoNode:
    return core.std.BlankClip(format=vs.RGB24, width=160, height=120, length=10)


def test_basic(gray_clip: vs.VideoNode) -> None:
    res = core.knlm.KNLMeansCL(gray_clip)
    assert res.format.id == gray_clip.format.id
    assert res.width == gray_clip.width
    assert res.height == gray_clip.height


@pytest.mark.parametrize("d", [0, 1, 2])
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("s", [0, 1, 4])
def test_radii(gray_clip: vs.VideoNode, d: int, a: int, s: int) -> None:
    res = core.knlm.KNLMeansCL(gray_clip, d=d, a=a, s=s)
    assert res.num_frames == gray_clip.num_frames


@pytest.mark.parametrize("h", [0.5, 1.2, 5.0])
def test_strength(gray_clip: vs.VideoNode, h: float) -> None:
    res = core.knlm.KNLMeansCL(gray_clip, h=h)
    assert res.num_frames == gray_clip.num_frames


@pytest.mark.parametrize("channels", ["Y", "auto"])
def test_channels_gray(gray_clip: vs.VideoNode, channels: str) -> None:
    res = core.knlm.KNLMeansCL(gray_clip, channels=channels)
    assert res.num_frames == gray_clip.num_frames


@pytest.mark.parametrize("channels", ["Y", "UV", "YUV", "auto"])
def test_channels_yuv(yuv_clip: vs.VideoNode, channels: str) -> None:
    res = core.knlm.KNLMeansCL(yuv_clip, channels=channels)
    assert res.num_frames == yuv_clip.num_frames


@pytest.mark.parametrize("channels", ["RGB", "auto"])
def test_channels_rgb(rgb_clip: vs.VideoNode, channels: str) -> None:
    res = core.knlm.KNLMeansCL(rgb_clip, channels=channels)
    assert res.num_frames == rgb_clip.num_frames


@pytest.mark.parametrize("wmode", [0, 1, 2, 3])
@pytest.mark.parametrize("wref", [0.0, 0.5, 1.0])
def test_weight(gray_clip: vs.VideoNode, wmode: int, wref: float) -> None:
    res = core.knlm.KNLMeansCL(gray_clip, wmode=wmode, wref=wref)
    assert res.num_frames == gray_clip.num_frames


@pytest.mark.parametrize("device_type", ["auto", "cpu", "gpu"])
def test_device_type(gray_clip: vs.VideoNode, device_type: str) -> None:
    # This might fail if the specific device type is not available,
    # but "auto" should always work if the plugin loaded.
    try:
        res = core.knlm.KNLMeansCL(gray_clip, device_type=device_type)
        assert res.num_frames == gray_clip.num_frames
    except vs.Error:
        if device_type == "auto":
            raise
        pytest.skip(f"Device type {device_type} not available")


def test_device_id(gray_clip: vs.VideoNode) -> None:
    res = core.knlm.KNLMeansCL(gray_clip, device_id=0)
    assert res.num_frames == gray_clip.num_frames


@pytest.mark.parametrize("ocl_x, ocl_y, ocl_r", [(0, 0, 0), (16, 8, 1)])
def test_ocl_tuning(gray_clip: vs.VideoNode, ocl_x: int, ocl_y: int, ocl_r: int) -> None:
    res = core.knlm.KNLMeansCL(gray_clip, ocl_x=ocl_x, ocl_y=ocl_y, ocl_r=ocl_r)
    assert res.num_frames == gray_clip.num_frames


def test_rclip(gray_clip: vs.VideoNode) -> None:
    rclip = core.std.BlankClip(gray_clip, color=[128])
    res = core.knlm.KNLMeansCL(gray_clip, rclip=rclip)
    assert res.num_frames == gray_clip.num_frames


def test_info(gray_clip: vs.VideoNode) -> None:
    res = core.knlm.KNLMeansCL(gray_clip, info=True)
    assert res.num_frames == gray_clip.num_frames


@pytest.mark.parametrize("mode", [0, 1, 2])
def test_mode_9_to_15bits(gray_clip: vs.VideoNode, mode: int) -> None:
    clip10 = core.std.BlankClip(format=vs.GRAY10, width=160, height=120, length=10)
    res = core.knlm.KNLMeansCL(clip10, mode_9_to_15bits=mode)
    assert res.format.bits_per_sample == 10


@pytest.mark.parametrize("bits", [8, 10, 16, 32])
@pytest.mark.parametrize("sample_type", [vs.INTEGER, vs.FLOAT])
def test_formats(bits: int, sample_type: vs.SampleType) -> None:
    if sample_type == vs.FLOAT and bits not in [16, 32]:
        pytest.skip("Unsupported float bit depth")
    if sample_type == vs.INTEGER and bits == 32:
        pytest.skip("Unsupported integer bit depth")

    fmt = core.std.BlankClip(
        width=160,
        height=120,
        format=core.std.BlankClip(format=vs.GRAY8).format.replace(bits_per_sample=bits, sample_type=sample_type),
    ).format
    clip = core.std.BlankClip(format=fmt, width=160, height=120, length=5)
    res = core.knlm.KNLMeansCL(clip)
    assert res.format.id == clip.format.id
