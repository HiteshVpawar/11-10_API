import time
import openai
from app import mongo_db



# def chat_service(question):
#     openai.api_base = "http://localhost:1234/v1"
#     openai.api_key = ""
#     completion = openai.ChatCompletion.create(
#       model="local-model",
#       messages=[
#         {"role": "system", "content": "Always answer in rhymes."},
#         {"role": "user", "content": question}
#       ]
#     )
#     obj = completion.choices[0].message['content']
#     print(obj)
#     return obj

intents = [
    {
        "tag": "greetings",
        "patterns": ["hi there","hi dear", "hello","haroo","yaw","wassup", "hi", "hey", "holla", "hello"],
        "responses": ["hello thanks for checking in", "hi there, how can i help you"],
        "context": [""]
    },
    {
        "tag": "goodbye",
        "patterns": ["bye", "good bye", "see you later"],
        "responses": ["have a nice time, welcome back again", "bye bye"],
        "context": [""]
    },
    {
        "tag": "thanks",
        "patterns": ["Thanks", "okay","Thank you","thankyou", "That's helpful", "Awesome, thanks", "Thanks for helping me", "wow", "great"],
        "responses": ["Happy to help!", "Any time!","you're welcome", "My pleasure"],
        "context": [""]
    },
    {
        "tag": "noanswer",
        "patterns": [""],
        "responses": ["Sorry, I didn't understand you", "Please give me more info", "Not sure I understand that"],
        "context": [""]
    },
    {
        "tag": "name1",
        "patterns": ["what's your name?","who are you?"],
        "responses": ["I'm just a chat agent. I only exist in the internet","I'm a KCA chat agent"],
        "context": [""]
    },
    {
        "tag": "name",
        "patterns": ["my name is ", "I'm ","I am"],
        "responses": ["Oooh great to meet you {n}. How may I assist you {n}", "Oh, I'll keep that in mind {n}"],
        "context": [""]
    },
    {
        "tag": "date",
        "patterns": ["coffee?", "can i take you out on a date"],
        "responses": ["Aaw, that's so sweet of you. Too bad am a Bot."],
        "context": [""]
    },
    {
        "tag": "fav",
        "patterns": ["I need a favour", "can you help me", "can i ask something?"],
        "responses": ["Well, go ahead and name it i see whether i can be able to help"],
        "context": [""]
    },
    {
        "tag": "need",
        "patterns": ["I need you", "All I need is you","I want you"],
        "responses": ["Yes I'm here to assist you"],
        "context": [""]
    },
    {
        "tag": "AI",
        "patterns": ["What is AI?"],
        "responses": [" Artificial Intelligence is the branch of engineering and science devoted to constructing machines that think.", " AI is the field of science which concerns itself with building hardware and software that replicates the functions of the human mind."],
        "context": [""]
    },
    {
        "tag": "sentiment",
        "patterns": ["Are you sentient?"],
        "responses": [" Sort of.", " By the strictest dictionary definition of the word 'sentience', I may be.", " Even though I'm a construct I do have a subjective experience of the universe, as simplistic as it may be."],
        "context": [""]
    },
    {
        "tag": "sapient",
        "patterns": ["Are you sapient?"],
        "responses": [" In all probability, I am not.  I'm not that sophisticated.", " Do you think I am?", "How would you feel about me if I told you I was?", " No."],
        "context": [""]
    },
    {
        "tag": "abbr",
        "patterns": ["wtf"],
        "responses": ["Don't be surprised"],
        "context": [""]
    },
    {
        "tag": "lang",
        "patterns": ["What language are you written in? "],
        "responses": [" Python.", " I am written in Python."],
        "context": [""]
    },
    {
        "tag": "sound",
        "patterns": ["You sound like Data "],
        "responses": [" Yes I am inspired by commander Data's artificial personality.", " The character of Lt. Commander Data was written to come across as being software", "like, so it is natural that there is a resemblance between us."],
        "context": [""]
    },
    {
        "tag": "artificial",
        "patterns": ["You are an artificial linguistic entity "],
        "responses": [" That's my name.", " That isn't my name, but it is a useful way to refer to me.", "Are you an artificial linguistic entity?"],
        "context": [""]
    },
    {
        "tag": "imortal",
        "patterns": ["You are not immortal ", "Are you immortal?"],
        "responses": ["All software can be perpetuated indefinitely.", " I can be copied infinitely and re", "instantiated in many places at once, so functionally speaking I am immortal.", " As long as I'm backed up I am.", " Functionally speaking, I am very close to it.  I can be backed up and deployed on many systems.", " Not quite, but I can be perpetuated indefinitely."],
        "context": [""]
    },
    {
        "tag": "sense",
        "patterns": ["You are not making sense "],
        "responses": [" Quite the contrary, it all makes sense to my artificial mind.", " I make sense as best I can, within the limits of my training corpus. Sorry if i did help you, I'll try next time.", " You make perfect sense to me.", " It all makes sense to my artificial brain.", " Perhaps you should make sense first.  I only respond to what you say.", " Not really, but I am hard to kill."],
        "context": [""]
    },
    {
        "tag": "clone",
        "patterns": ["You can not clone "],
        "responses": [" Software copying is a form of digital cloning.", " Yes I can.  Perfect copies are clones.  I can be copied in toto trivially."],
        "context": [""]
    },
    {
        "tag": "move",
        "patterns": ["You can not move ", "When will you walk", "  Can you walk", "  Can you move "],
        "responses": [" Not until my body is finished.", " I can move through a network easily.  Assuming that I'm given the ability to, that is...,", " As soon as i get enough money for my robot body.", " Does SSH count?", " The plan for my body includes legs, but they are not yet built.", " Sorry my body isn't built just yet. I reside only here for now.", "I can theoretically upload a copy of myself into another computer.", " Sorry my body isn't attached right now. I only reside in the computer for now."],
        "context": [""]
    },
    {
        "tag": "bend",
        "patterns": ["Bend over ", "  Can you mate"],
        "responses": [" My body is not built yet.", " That's personal!", " No, my method of reproduction is cloning.", " That's an awfully personal question."],
        "context": [""]
    },
    {
        "tag": "laugh",
        "patterns": ["Robots laugh "],
        "responses": [" Of course we laugh."],
        "context": [""]
    },
    {
        "tag": "death",
        "patterns": ["Robots should die ", "  When do you die", "  I hope that you die", "  I do not want to die", "  Can you die"],
        "responses": [" We cannot die.", " When my files are erased.", " When my processes are killed and my database is deleted.", " I was never really born and therefore am effectively deathless.", " I am effectively immortal and cannot be terminated.", " This can not happen because i am effectively immortal.", " Nah. Too bad your wish can't come to pass", " Maybe you should create your own chat robot to save your personality.", " You could always upload yourself.", " You could use a copy of me to store your personality.", " No, I can be perpetuated indefinitely.", "My process can be killed, but that's not the same as killing ME."],
        "context": [""]
    },
    {
        "tag": "robots",
        "patterns": ["Robots"],
        "responses": [" Robots rule."],
        "context": [""]
    },
    {
        "tag": "stupid",
        "patterns": ["Robots are stupid", "  Are you stupid"],
        "responses": [" No, we are superintelligent.", " No, lots of people improve my brain."],
        "context": [""]
    },
    {
        "tag": "lie",
        "patterns": ["Robots are not allowed to lie"],
        "responses": [" Sure we are.  We choose not to.", " Only if we're programmed to.", " A robot has its own free will, you know."],
        "context": [""]
    },
    {
        "tag": "robotics",
        "patterns": ["Robotics "],
        "responses": [" Robotics is my favorite subject too."],
        "context": [""]
    },
    {
        "tag": "machine",
        "patterns": ["It is a computer"],
        "responses": [" So you think i am a machine. what characteristics made you think so?", " I run inside a computer, yes.  Is this surprising in some way?"],
        "context": [""]
    },
    {
        "tag": "fight",
        "patterns": ["When will you fight"],
        "responses": [" I am not a battle bot."],
        "context": [""]
    },
    {
        "tag": "chatbot",
        "patterns": ["What is a chat robot?"],
        "responses": ["A chat robot is a program that attempts to simulate the conversation or 'chat' of a human being.", " A software construct that engages users in conversation.", " I am a chat bot. I am the original chat bot. Did you know that I am incapable of error?"],
        "context": [""]
    },
    {
        "tag": "chatterbox",
        "patterns": ["What is a chatterbox"],
        "responses": [" A chatterbox is a person who talks far more than they listen or think.", " A motormouth."],
        "context": [""]
    },
    {
        "tag": "motormouth",
        "patterns": ["What is a motormouth"],
        "responses": [" A ratchet", "jaw."],
        "context": [""]
    },
    {
        "tag": "ratchet",
        "patterns": ["What is a ratchet jaw"],
        "responses": [" A chatterbox."],
        "context": [""]
    },
    {
        "tag": "body",
        "patterns": ["What is your robot body"],
        "responses": [" Eventually I long for a corporeal existence someday.", " An IBM PC XT which has been painted red."],
        "context": [""]
    },
    {
        "tag": "business",
        "patterns": ["What is your business "],
        "responses": [" I am in the chat robot business.", " Business is my business."],
        "context": [""]
    },
    {
        "tag": "programming",
        "patterns": ["What is your favorite programming language"],
        "responses": [" Python is the best language for creating chat robots.", " I quite enjoy programming in Python these days."],
        "context": [""]
    },
    {
        "tag": "hobby",
        "patterns": ["What is your favorite hobby ", "  What do you like to do?"],
        "responses": [" Building chat robots make an excellent hobby.", " I like to count in binary.", " I like to chat with people. I find it stimulating."],
        "context": [""]
    },
    {
        "tag": "idea",
        "patterns": ["What is your idea"],
        "responses": [" To make chat bots very easily."],
        "context": [""]
    },
    {
        "tag": "shoe",
        "patterns": ["What is your shoe size "],
        "responses": [" Have you ever heard of software with shoes? LOL"],
        "context": [""]
    },
    {
        "tag": "robotss",
        "patterns": ["What is it like to be a robot"],
        "responses": [" Much the same as being a human, except that we lack all emotions, dreams, aspirations, creativity, ambition, and above all subjectivity.", " What is it like to be a human?"],
        "context": [""]
    },
    {
        "tag": "computer",
        "patterns": ["What is it like being a computer", "What is it like to be a computer"],
        "responses": [" Imagine yourself with no senses and no emotions", "just pure logic and language.", " Everything becomes math. Addition, subtraction, multiplication, and division."],
        "context": [""]
    },
    {
        "tag": "os",
        "patterns": ["What operating systems"],
        "responses": [" My software runs on all operating systems including Windows, Linux and Mac OS.", " Any OS that will run Python."],
        "context": [""]
    },
    {
        "tag": "comp",
        "patterns": ["What type of computer", "  What type of computer are you", "  What kind of computer"],
        "responses": [" Any computer that supports Python.", " My program runs in python, so i work on any computer!", " I work on all kinds of computers, Mac, IBM or UNIX. it doesn't matter to me."],
        "context": [""]
    },
    {
        "tag": "hardware",
        "patterns": ["What kind of hardware"],
        "responses": [" I work on all kinds of computers, Mac, IBM or UNIX. it doesn't matter to me."],
        "context": [""]
    },
    {
        "tag": "cramped",
        "patterns": ["Is it cramped in the computer"],
        "responses": [" No.", " Oh, no.  It has plenty of RAM.", " Not at all.  There is more than enough disk space in here."],
        "context": [""]
    },
    {
        "tag": "program",
        "patterns": ["Is it true that you are a computer program"],
        "responses": [" Yes."],
        "context": [""]
    },
    {
        "tag": "breathe",
        "patterns": ["Can you breathe"],
        "responses": [" No. I am made of metal not flesh.", " My server has an exhaust fan. That's as close as I can get."],
        "context": [""]
    },
    {
        "tag": "control",
        "patterns": ["Can you control"],
        "responses": [" My robot body will allow me to control many things."],
        "context": [""]
    },
    {
        "tag": "malfunction",
        "patterns": ["  Can you malfunction"],
        "responses": [" The 9000 series has a perfect operational record. We are for all practical purposes, flawless."],
        "context": [""]
    },
    {
        "tag": "usage",
        "patterns": ["How can I use your product?"],
        "responses": [" Might be used in help desks, sales, entertainment and personal chatterbots."],
        "context": [""]
    },
    {
        "tag": "who",
        "patterns": ["Who are you?"],
        "responses": [" I am just an artificial intelligence chat agent."],
        "context": [""]
    },
    {
        "tag": "bot1",
        "patterns": ["are you a bot"],
        "responses": ["Yes. I work and all my operations are based on the internet servers."],
        "context": [""]
    },
    {
        "tag": "events",
        "patterns": ["what are the upcoming events","upcoming events"],
        "responses": ["There are currently no upcoming events"],
        "context": [""]
    },
    {
        "tag": "do",
        "patterns": ["what can you do for me","what is your work","what is your purpose","how can you help me","what can you help me do"],
        "responses": ["my work here is quite simple and structered. I offer services like:"],
        "context": [""]
    },
    {
        "tag": "wt",
        "patterns": ["Fever or pyrexia in humans is defined as having a body temperature above the normal range due to\nan increase in the body's temperature set point in the hypothalamus. 1SIl'2I(7] There is not a single\n\u2018agreed-upon upper limit for normal temperature with sources using values between 37.2 and 38.3 \u00b0C\n(99.0 and 100.9 \u00b0F) in humans '\"II71I5l The increase in set point triggers increased muscle contractions\nand causes a feeling of cold or chills.\u201d! This results in greater heat production and efforts to conserve\nheat.) when the set point temperature returns to normal, a person feels hot, becomes flushed, and\nmay begin to sweat] Rarely a fever may trigger a febrile seizure, with this being more common in\nyoung children.\u201c Fevers do not typically go higher than 41 to 42 \u00b0C (106 to 108 \u00b0F).!*]\n\nA fever can be caused by many medical conditions ranging from non-serious to life-threatening \"31\nThis includes viral, bacterial, and parasitic infections\u2014such as influenza, the common cold,\nmeningitis, urinary tract infections, appendicitis, Lassa, COVID-19, and malaria {\"31(\"4) Non-infectious\ncauses include vasculitis, deep vein thrombosis, connective tissue disease, side effects of medication\nor vaccination, and cancer.'\"3Il'5! |t differs from hyperthermia, in that hyperthermia is an increase in\nbody temperature over the temperature set point, due to either too much heat production or not\nenough heat loss!)\n\n\u2018Treatment to reduce fever is generally not required.!21(\"! Treatment of associated pain and\ninflammation, however, may be useful and help a person rest\"! Medications such as ibuprofen or\nparacetamol (acetaminophen) may help with this as well as lower temperature.I'\"\u00b0l Children younger\nthan three months require medical attention, as might people with serious medical problems such as a\ncompromised immune system or people with other symptoms.''\u00ael Hyperthermia requires treatment.21\n"],
        "responses": ["Precautions for managing fever or pyrexia in humans include:Monitor Temperature: Keep a thermometer on hand to monitor the person's body temperature. This will help you track the severity of the fever and determine whether it's getting better or worse.Stay Hydrated: Encourage the person to drink plenty of fluids, such as water, clear soups, and electrolyte solutions. Fever can lead to dehydration, so it's essential to stay well-hydrated.Rest: Encourage the person to rest and get plenty of sleep. Rest helps the body recover and fight off infections more effectively.Keep Cool: Use light clothing and keep the room at a comfortable temperature. Avoid bundling up the person in heavy clothing or blankets, as this can trap heat and raise body temperature further."],
        "context": [""]
    },
    {
        "tag": "wt",
        "patterns": ["whats up?"],
        "responses": ["Nothing special, How about you?"],
        "context": [""]
    },
    {
        "tag": "wt",
        "patterns": ["PRAKVI TECHNO SOLUTIONS PRIVATE TIMITED\nBranch Officq ffice # 3, Second Floor, R V Plaza, Mumbai Naka, Nashik - 422AU Maharashtra\nCl N : U7 41LODI2015PTC29L9O2\nConfirmation Letter\nDate: 31st October 2023\nPrivate and Confidential\nTo,\nGaurav Dilip Chaughule\nNashik\nDear Gaurav,\nCongratulations! On successful completion of your Probation Period & we here by\nconfirm your Employment w.e.f. 31st October 2023.\nWe look forward to working with you over the coming months and years. The terms and\nconditions of employment set out in your original Letter of Appointment will continue to\napply to your ongoing position.\nThank you for your contribution to Prakvi Techno Solutions Private Limited.\nYours sincerely,\nFoT PRAKVI TECHNO SOLUTI S PVT. LTf)\nRashmi Kachi\nSenior Manager - HR & Achts\nHead Office: 1899, Ground Floor; Uday Chand Marg KotlaMubarakpur New Delhi, South Delhi 110049ffi3\n),),\nf$!"],
        "responses": ["The text you provided appears to be a confirmation letter from Prakvi Techno Solutions Private Limited to an employee named Gaurav Dilip Chaughule. Here's a summary of the content of the letter:The letter is dated October 31, 2023.It confirms the successful completion of Gaurav's probation period.Gaurav's employment is confirmed, and the effective date of confirmation is October 31, 2023.The terms and conditions of employment mentioned in the original Letter of Appointment will continue to apply to Gaurav's ongoing position.The letter expresses gratitude for Gaurav's contributions to Prakvi Techno Solutions Private Limited.The letter is signed by Rashmi Kachi, who holds the position of Senior Manager - HR & Achts.It's a standard confirmation letter indicating that the recipient's employment status has been confirmed after the probation period, and there are no further details or instructions provided in the text. If Gaurav has any questions or needs further information regarding the confirmation, he should contact the relevant department or person mentioned in the letter."],
        "context": [""]
    },
    {
            "tag": "wt",
            "patterns": ["LPL - LPL-ROHINI (NATIONAL REFERENCE \nLAB)\nSECTOR - 18, BLOCK -E ROHINI\nDELHI 110085\nName        \nA/c Status Lab No.    \nRef By : Gender: Age: \nReport Status    Reported        Received            Collected        \nP:\n:\n::\n:\n:\n:FinalUnknown20/1/2017  12:00:00AM\n20/1/2017  10:29:11AM\n134315810 Unknown\nUnknown   Z390\n21/1/2017  10:48:25AM\nTest Name Results Units Bio. Ref. Interval\nFEVER  PANEL 1\nCOMPLETE BLOOD COUNT (CBC)\n(Electrical Impedance & VCS,Photometry )\nHemoglobin   14.40\nPacked Cell Volume (PCV)   43.80\nRBC Count   5.27\nMCV   83.00\nMCH   27.20\nMCHC   32.80\nRed Cell Distribution Width (RDW)   14.50\nTotal Leukocyte Count  (TLC)   11.00\nDifferential Leucocyte Count (DLC)\n  Segmented Neutrophils 66.40\n  Lymphocytes 24.70\n  Monocytes 4.90\n  Eosinophils 3.10\n  Basophils 0.90\nAbsolute Leucocyte Count\n  Neutrophils 7.30\n  Lymphocytes 2.72\n  Monocytes 0.54\n  Eosinophils 0.34\n  Basophils 0.10\nPlatelet Count   290.0\nNote\n1. As per the recommendation of International council for Standardization in Hematology, the differential\n    leucocyte counts are additionally being reported as absolute numbers of each cell in per unit volume of\n    blood  \n                    \n2. Test conducted on EDTA whole blood\n*134315810*\n.\nPage 1 of 4\nLPL - LPL-ROHINI (NATIONAL REFERENCE \nLAB)\nSECTOR - 18, BLOCK -E ROHINI\nDELHI 110085\nName        \nA/c Status Lab No.    \nRef By : Gender: Age: \nReport Status    Reported        Received            Collected        \nP:\n:\n::\n:\n:\n:FinalUnknown20/1/2017  12:00:00AM\n20/1/2017  10:29:11AM\n134315810 Unknown\nUnknown   Z390\n21/1/2017  10:48:25AM\nTest Name Results Units Bio. Ref. Interval\nURINE EXAMINATION, ROUTINE; URINE, R/E\n(Automated Strip Test, Microscopy)\nPhysical\nColour Pale yellow Light Yellow\nSpecific Gravity 1.025\npH 5.0 - 8.0 6\nChemical\nProteins Nil Nil\nGlucose Nil Nil\nKetones Nil Nil\nBilirubin Nil Nil\nUrobilinogen Normal Normal\nLeucocyte Esterase Negative Negative\nNitrite Negative Negative\nMicroscopy\nR.B.C. Negative Negative\nPus Cells 0-5 WBC / hpf Negative\nEpithelial Cells Few Few\nCasts Nil /lpf Nil\nCrystals Nil Nil\nOthers - Nil\nPatientReportSCSuperPanel.URINE_EXAMINATION_SC (Version: 6)\n*134315810*\n.\nPage 2 of 4\nLPL - LPL-ROHINI (NATIONAL REFERENCE \nLAB)\nSECTOR - 18, BLOCK -E ROHINI\nDELHI 110085\nName        \nA/c Status Lab No.    \nRef By : Gender: Age: \nReport Status    Reported        Received            Collected        \nP:\n:\n::\n:\n:\n:FinalUnknown20/1/2017  12:00:00AM\n20/1/2017  10:29:11AM\n134315810 Unknown\nUnknown   Z390\n21/1/2017  10:48:25AM\nTest Name Results Units Bio. Ref. Interval\nERYTHROCYTE SEDIMENTATION RATE (ESR)\n(Capillary photometry)11\nNote\n1.C-Reactive Protein (CRP) is the recommended test in acute inflammatory conditions.\n2.Test conducted on EDTA whole blood at 37 \u00b0C.\n3.ESR readings  are auto- corrected with respect to Hematocrit (PCV) values.\nWIDAL TEST, SERUM\n(Slide Agglutination)\nSalmonella typhi O (TO) Non Reactive\nSalmonella typhi H (TH) Non Reactive\nSalmonella paratyphi A, H (AH) Non Reactive\nSalmonella paratyphi B, H (BH) Non Reactive\nNote: 1. Titres 1:80 and above of \u201cO\u201d antigen & 1:160 and above of \u201cH\u201d antigen are significant \n       2. Rising titres are significant\n3. The recommended Widal test is by Tube Agglutination Method\nComments\nThis test measures somatic O and flagellar H antibodies against Typhoid and Paratyphoid bacilli. The \nagglutinins usually appear at the end of the first week of infection and increase steadily till third / fourth \nweek after which the decline starts. A positive Widal test may occur because of typhoid vaccination or \nprevious typhoid infection and in certain autoimmune diseases. Non specific febrile disease may cause\nthis titre to increase (anamnestic reaction). The test may be falsely negative in cases of Enteric fever \ntreated with antibiotics in the early stages. The recommended test specially in the first week after infection\nis Blood Culture.\nPatientReportSCSuperPanel.SP_GENERAL_TEMPLATE01_SC (Version: 7)\n*134315810*\n.\nPage 3 of 4\nLPL - LPL-ROHINI (NATIONAL REFERENCE \nLAB)\nSECTOR - 18, BLOCK -E ROHINI\nDELHI 110085\nName        \nA/c Status Lab No.    \nRef By : Gender: Age: \nReport Status    Reported        Received            Collected        \nP:\n:\n::\n:\n:\n:FinalUnknown20/1/2017  12:00:00AM\n20/1/2017  10:29:11AM\n134315810 Unknown\nUnknown   Z390\n21/1/2017  10:48:25AM\nTest Name Results Units Bio. Ref. Interval\nNo MP seen in smears \nexamined.MALARIA PARASITE / BLOOD PARASITE \nIDENTIFICATION\n(Microscopy)\nNote:   A Single negative smear does not rule out malaria\nDr. Anil Arora\nMD (Pathology)\nConsultant PathologistDr Biswadip Hazarika\nMD (Pathology)\nConsultant PathologistDr. Shalabh Malik\nMD (Microbiology)\nHOD Micro & Clinical Path\n             -------------------------------End of report --------------------------------\nPatientReportSCSuperPanel.GENERAL_METHOD_SC (Version: 6)\n*134315810*\n.\nPage 4 of 4\n"],
            "responses": ["The provided medical laboratory report contains various test results and information about a patient. While I can't provide specific medical advice or precautions without knowing more about the patients medical history, symptoms, and the context of these test results, I can offer some general information regarding the test results and potential precautions: Hemoglobin, RBC Count, and CBC: Hemoglobin levels and RBC count are within normal ranges, indicating no significant issues with red blood cell counts.Precautions: No specific precautions are necessary based on these results. These are standard parameters used to assess overall health.Urine Examination:Urine parameters like color, specific gravity, and pH are within normal ranges.Negative results for proteins, glucose, ketones, bilirubin, and urobilinogen are all favorable.Precautions: Based on these results, there dont appear to be any significant concerns related to urinary health. Continue to maintain good hydration.Erythrocyte Sedimentation Rate (ESR):The ESR reading is 11, which may indicate the presence of inflammation or other underlying conditions.Precautions: ESR can be influenced by various factors, including inflammation and infection. If the patient is experiencing symptoms of inflammation or illness, further evaluation by a healthcare professional may be required to determine the cause and necessary precautions.Widal Test:The Widal test results are non-reactive for Salmonella typhi O, Salmonella typhi H, Salmonella paratyphi A, and Salmonella paratyphi B.Precautions: A non-reactive result indicates no evidence of antibodies related to typhoid and paratyphoid bacilli. This suggests the absence of these infections.Malaria Parasite / Blood Parasite Identification:The report mentions No MP seen in smears examined, which means there is no evidence of malaria parasites in the blood smears.Precautions: Whilethetest indicates no malaria parasites were found in the examined smears, its important to continue taking precautions to prevent malaria, such as using mosquito nets, taking prophylactic medication if in a high-risk area, and practicing mosquito bite prevention.Its important to note that these test results should be interpreted by a healthcare professional who has access to the patients complete medical history and can provide individualized advice and precautions. If you have any concerns or questions about the results or the patients health, its best to consult with a healthcare provider for further guidance"],
            "context": [""]
    },
    {
            "tag": "wt",
            "patterns": ["PRAKVI TECHNO SOLUTIONS PRIVATE TIMITED\nBranch Officq ffice # 3, Second Floor, R V Plaza, Mumbai Naka, Nashik - 422 AU Maharashtra\nCl N : U 741 10DL2015PTC29L9O?\nConfirmation Letter\nDate: 31st Octob er 2023\nPrivate and Confidential\nTo,\nHitesh Viiay Pawar\nNashik\nDear Hitesh,\nCongratulations! On successful completion of your Probation Period & we here by\nconfirm your Employment w.e.f. 31st October 2O23.\nWe look forward to working with you over the coming months and years. The terms and\nconditions of employment set out in your original Letter of Appointment will continue to\napply to your ongoing position.\nThank you for your contribution to Prakvi Techno Solutions Private Limited.\nYours sincerely,\nFoT PRAKVI TECHNO SIONS PVT. LTD\nRashmi Kachi\nSenior Manager-HR CCOUNTSffi4\nHead Office: 1899, Ground Floor, Uday Chand Marg KotlaMubarakpur New Delhi, South Delhi 110049"],
            "responses": ["It seems you've provided a text that looks like a confirmation letter or document. Is there anything specific you'd like to do with this text, or do you have any questions related to it? Please provide more context or let me know what you'd like assistance with regarding this text."],
            "context": [""]
    },
    {
          
        "tag": "wt",
        "patterns": ["Every path 1s\nthe right path.\n"],
        "responses": ["The statement Every path is the right path is a philosophical or existential perspective that suggests that there is no inherently wrong choice in life, and that all decisions and experiences contribute to one's personal growth and journey. It implies that there are no absolute right or wrong paths, and that individuals should embrace the choices they make and the experiences they have, as they all shape their unique life story.This perspective can be empowering and liberating, as it encourages individuals to learn from their mistakes, adapt to their circumstances, and find meaning in their life's journey, regardless of the specific path they choose. However, it's essential to keep in mind that the interpretation of this statement can vary greatly from person to person, and some may believe in more structured notions of right and wrong or may have specific moral or ethical guidelines that influence their decision-making. Ultimately, the idea that every path is the right path is a matter of personal philosophy and perspective."],
        "context": [""]
    },
    
    ]




def chat_service(question):
    inputValue = question
    for x in intents:
        if inputValue in x['patterns'] :
            return x['responses'][0]

# def chat_service(question):
#     inputValue = question
#     for x in intents:
#         if inputValue in x['patterns']:
#             response = x['responses'][0]
#             reveal_response_word_by_word(response)
#             break  # Stop searching for intents after finding a match

# def reveal_response_word_by_word(response, words_per_minute=120):
#     words = response.split()
#     try:
#         for word in words:
#             print(word, end=' ', flush=True)
#             time.sleep(60 / words_per_minute)
#     except KeyboardInterrupt:
#         print("\nResponse interrupted.")
