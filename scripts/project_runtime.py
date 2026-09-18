"""Portable locations for checked-in results, Node.js, and Chinese plot fonts."""
from pathlib import Path
import os
import shutil


def raw_output_dir(run_dir, metadata):
    """Prefer data beside result.json after cloning; retain legacy compatibility."""
    run_dir = Path(run_dir)
    recorded = str(metadata.get('output_dir', ''))
    name = recorded.replace('\\', '/').rstrip('/').split('/')[-1]
    candidate = run_dir / name
    if name.endswith('.raw') and candidate.is_dir():
        return candidate
    candidates = sorted(p for p in run_dir.glob('*.raw') if p.is_dir())
    if len(candidates) == 1:
        return candidates[0]
    if not candidates and recorded and Path(recorded).is_dir():
        return Path(recorded)
    raise FileNotFoundError(f'Cannot uniquely locate PSF data beside {run_dir / "result.json"}')


def node_executable():
    node = shutil.which('node')
    if not node:
        raise RuntimeError('请安装 Node.js 并将 node 加入 PATH。')
    return node


def plot_font_families():
    """Find a CJK font on this machine, or accept an explicit local font file."""
    from matplotlib import font_manager
    explicit = os.environ.get('SANSEN_CJK_FONT')
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f'SANSEN_CJK_FONT does not exist: {path}')
        font_manager.fontManager.addfont(str(path))
        return ['DejaVu Sans', font_manager.FontProperties(fname=str(path)).get_name()]
    mac_font = Path('/System/Library/Fonts/Hiragino Sans GB.ttc')
    if mac_font.is_file():
        font_manager.fontManager.addfont(str(mac_font))
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in ['Noto Sans CJK SC', 'Noto Sans SC', 'Source Han Sans SC',
                 'Microsoft YaHei', 'SimHei', 'Hiragino Sans GB', 'PingFang SC']:
        if name in available:
            return ['DejaVu Sans', name]
    raise RuntimeError('未找到中文字体。请安装思源黑体／Noto Sans CJK，或设置 SANSEN_CJK_FONT 为字体文件路径。')
