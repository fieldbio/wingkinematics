original files, used for spinner paper

=======
Wingkinematics_v5.0 uses the wrong degrees of freedom for standard deviation calculations (0 vs 1). However this doesn't affect any of the data presented in the Spin Paper because the only standard deviations that were used were calculated in a spreadsheet. This applies to the Standard errors used in images 3 and 8, they are correct. This ddof problem was fixed in v5.3 which is used for the geese and the sideslip.

This is the oldest working version of this program and therefore the workflow is not streamlined. The input data must be the original data, already filtered and already upsampled as well as the pronation_supination file, already upsampled (for the spinner paper, Elsa did these steps). These two files are loaded into wingkinematics_upsample_v0.0.py which shows a graph of the wingstroke endpoints and outputs a new pronation_supination file. In later versions of the program the filtering and the upsampling is all done by my scripts.

