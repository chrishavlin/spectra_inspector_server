from spectra_inspector_server._file_tree_handling import EDAXPathHandler
from spectra_inspector_server.processor.file_loaders import load_edax_spd

ph = EDAXPathHandler()
C12files = ph.get_sample_edax_file_names("C-12")

ds = load_edax_spd(C12files)
