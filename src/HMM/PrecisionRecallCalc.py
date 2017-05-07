from src.HMM.ViterbiCorrector import ViterbiCorrector;
class PrecisionRecallCalc:

    def computePrecisionRecall(self,test_data,corrupted_test_data,spell_corrector_obj):
        total_data_size=len(test_data);
        TP=0;
        FP=0;
        FN=0;
        for word in corrupted_test_data:
            corrupted_word=True;
            index = corrupted_test_data.index(word);
            if word==test_data[index]:
                corrupted_word=False;
            corrected_word = spell_corrector_obj.word_corrector(word);
            if corrupted_word:
                if corrected_word == test_data[index]:
                    TP=TP+1;
                else:
                    FN=FN+1;
            else:
                if corrected_word != test_data[index]:
                    FP=FP+1;
        recall = TP/(float)(TP+FN);
        precision = TP/(float)(TP+FP);
        print "Total testing words:",total_data_size;
        print "Wrong ------> Correct(TP)",TP;
        print "Wrong -------> Wrong (FN)",FN;
        print "Precision---->",precision;
        print "Correct -----> Wrong(FP)",FP;
        print "Recall-------->",recall;





