#launch them on 4 parallel jobs in bkg
for i in 140 200 250 300; do python -u plot_occupancies.py ${i} > log_occupancyplots_${i}.txt 2>&1 &  done
