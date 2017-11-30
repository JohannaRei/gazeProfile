from analysisFunctions import *

plotStyle()

#Read control group files for both tasks, these will be the population against which the individuals will be scored
#Never change these, only the files in the controlData folder, if needed
control_srt_s, control_srt_a = get_controls('controlData', 'SRT')
control_face_s, control_face_a = get_controls('controlData', 'Face')

#NOTE: readFile should only be used to read in the control GROUP data, not individual subjects we want to compare to controls!

#Combine subject SRT and Face task datas into one subject DataFrame
datas = pd.merge(controlSRTS, controlFaceS, on='subject', how="right")
datas = removeSubjects(datas, ['TV33', 'TV59']) #Removing individual subjects happens with this function (or you can remove them completely from the original csv file)

#getStd(sA, datas) #get SRT standard deviations
#getCI(sA, datas) #get SRT confidence intervals (KESKEN!!)

#90. percentile for subject SRTs
wpr(sA, datas)

uudetBest = []
for i,r in datas.iterrows():
    p50 = r.SRTmed
    sub = sA[sA.subject == r.subject]
    subSRT = [value for value in sub.srtAll if not math.isnan(value)]
    bestSRT = [value for value in subSRT if value <= p50]
    uudetBest.append(np.mean(bestSRT))
datas['best_srt'] = uudetBest
datas["best_z"] = st.zscore(datas.best_srt)
print(np.mean(datas.best_srt))

#One way ANOVA for
fVal, pVal = st.f_oneway(datas.pfix_c, datas.pfix_n, datas.pfix_h, datas.pfix_f)
print("Pfix ANOVA F: " + str(fVal) + ", p-value: " + str(pVal))

#Deltas for each stimulus pair
pfixDeltas(datas)

#Test distribution normality, if normal --> fit quadratic regression curve to delta x the mean of the two pfix means
transformAll(datas)
#print("persentiilit")
#percPlots(datas)

plt.plot([np.mean(datas.pfix_c), np.mean(datas.pfix_n), np.mean(datas.pfix_h), np.mean(datas.pfix_f)], 'bo-')
plt.plot([np.mean(datas.comb_c), np.mean(datas.comb_n), np.mean(datas.comb_h), np.mean(datas.comb_f)], 'ro-')
plt.axis([-0.5,3.5,0,1])
plt.xticks([0,1,2,3], ["Kontrolli", "Neutraali", "Iloinen", "Pelokas"])
plt.xlabel("Kasvojen ilme")
plt.ylabel("Katseluosuus")
plt.show()

#saveFile(datas, "verrokit.csv")

#printAllProfiles(datas)

#TOIBILAS
#tSS, tSA = readToibFile(['epi9_2_SRT.csv'], 'SRT') #filenames of preprocessed SRT-data
#tFS, tFA = readToibFile(['dtbt_toibilas_face_25s.csv', 'dtbt_toibilas_srt_28s.csv', 'dtbt_toibilas_srt_33s.csv'], 'Face')

#print(tSS)
#print(tSA)
#tdatas = pd.merge(tSS, tFS, on='subject', how="right")
#tdatas = tdatas[(tdatas.subject != 'Toib36') & (tdatas.subject != 'Toib25') & (tdatas.index != 2)]
#wpr(tSA, tdatas)
#pfixDeltas(tdatas)
#transformToib(tdatas)
