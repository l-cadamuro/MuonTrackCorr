# for i in {1..10}; do python fit_windows.py $i corr_fits/matching_windows_phi.root 1 0; done ## phi windows, fitting as A + 1/pt^B
# for i in {1..10}; do python fit_windows.py $i corr_fits/matching_windows_theta.root 1 1; done ## theta windows, fitting as A + 1/pt^B

# for i in {1..10}; do python fit_windows.py $i corr_fits/matching_windows_phi_q90.root 1 0 90; done ## phi windows, fitting as A + 1/pt^B
# for i in {1..10}; do python fit_windows.py $i corr_fits/matching_windows_theta_q90.root 1 1 90; done ## theta windows, fitting as A + 1/pt^B

# for i in {1..10}; do python fit_windows.py $i corr_fits/matching_windows_phi_q99.root 1 0 99; done ## phi windows, fitting as A + 1/pt^B
# for i in {1..10}; do python fit_windows.py $i corr_fits/matching_windows_theta_q99.root 1 1 99; done ## theta windows, fitting as A + 1/pt^B


# for i in {1..10}; do python fit_windows.py --binN $i --rootOut corr_fits/matching_windows_phi.root --plotType 0; done ## phi windows, fitting as A + 1/pt^B
# for i in {1..10}; do python fit_windows.py --binN $i --rootOut corr_fits/matching_windows_theta.root --plotType 1; done ## theta windows, fitting as A + 1/pt^B

# for i in {1..10}; do python fit_windows.py --binN $i --rootOut corr_fits/matching_windows_phi_q90.root --plotType 0 --quantile 90; done ## phi windows, fitting as A + 1/pt^B
# for i in {1..10}; do python fit_windows.py --binN $i --rootOut corr_fits/matching_windows_theta_q90.root --plotType 1 --quantile 90; done ## theta windows, fitting as A + 1/pt^B

# for i in {1..10}; do python fit_windows.py --binN $i --rootOut corr_fits/matching_windows_phi_q99.root --plotType 0 --quantile 99; done ## phi windows, fitting as A + 1/pt^B
# for i in {1..10}; do python fit_windows.py --binN $i --rootOut corr_fits/matching_windows_theta_q99.root --plotType 1 --quantile 99; done ## theta windows, fitting as A + 1/pt^B


################## for barrel and overlap studies

for i in {1..10}; do python fit_windows.py --binN $i --rootOut prova_matching_windows_phi_q99.root --plotType 0 --quantile 99; done ## phi windows, fitting as A + 1/pt^B
for i in {1..10}; do python fit_windows.py --binN $i --rootOut prova_matching_windows_theta_q99.root --plotType 1 --quantile 99; done ## theta windows, fitting as A + 1/pt^B
