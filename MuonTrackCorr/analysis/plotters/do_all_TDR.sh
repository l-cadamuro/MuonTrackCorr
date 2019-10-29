for i in {0..3}; do python plot_rate_TDR.py $i ; done
for i in 0 1 2 3; do python rate_vs_PU.py $i ; done
source drawAllEffPlots.sh
python plot_matching_windows.py
for i in {0..3}; do python resolution_plots_TDR.py $i ; done
