# Baseline Intent Evaluation Report

## Dataset
- **Size**: 200 examples
- **Unambiguous**: 168
- **Ambiguous**: 32

## Overall Metrics
- **Accuracy**: 0.4750
- **Macro F1**: 0.4223
- **Macro Precision**: 0.5963
- **Macro Recall**: 0.4104

## Ambiguity Split
- **Unambiguous Accuracy**: 0.4881 (Macro F1: 0.4221)
- **Ambiguous Accuracy**: 0.4062 (Macro F1: 0.1616)

## Representative Errors
Showing up to 20 mismatched examples:

### GOLDEN_002
**Message**: @AppleSupport you seem to be skipping the step that allows to select which carrier phone to get for iPhone X upgrade head start. Why?
- **Gold**: Purchase & Store Operations
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_003
**Message**: Bruhhhh I’m so fuckin tired @AppleSupport @115858 fixed these damn glitches ! Keep cutting my phone off
- **Gold**: Device Performance / Hardware
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: True
- **Notes**: Multiple device symptoms plus frustration; primary action is device troubleshooting.

### GOLDEN_004
**Message**: What is this “A” and  QUESTION MARK THAT MY PHONE KEEPS DOING!! @115858 @AppleSupport
- **Gold**: Software Bug / Glitch
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_006
**Message**: WHY IS THE LETTER I SHOWING UP AS A QUESTION MARK IN A BOX ? @115858 FIX IT
- **Gold**: Software Bug / Glitch
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_007
**Message**: @AppleSupport trying to setup HomeKit automation for when multiple people leave home but it says to upgrade my hub -an Apple TV w tvOS 11.1 https\\://t.co/IXpgmAi9vc
- **Gold**: How-To / Feature Question
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_008
**Message**: Love how my $1200 @115858 iPhone X constantly freezes when using apps like YouTube and Apple Music. Wtf
- **Gold**: Device Performance / Hardware
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_010
**Message**: @AppleSupport with iOS11 my phone won’t show my music on my lock screen and when I receive calls I can’t hear anything on the other end help
- **Gold**: Software Bug / Glitch
- **Predicted**: Device Performance / Hardware
- **Ambiguous**: True
- **Notes**: Two distinct post-update failures (music/phone calls); primary intent requires judgment.

### GOLDEN_011
**Message**: @AppleSupport  I updated to iOS 11.0.3 on my 6s plus &amp; I just went from 85% to 13% in an hour after watching two YouTube videos. :/
- **Gold**: Device Performance / Hardware
- **Predicted**: Software Bug / Glitch
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_014
**Message**: @AppleSupport Any idea when the @ATT activation servers will stop shitting themselves, or do I keep mashing Try Again &amp; hope? #iphoneXlaunch
- **Gold**: Purchase & Store Operations
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_015
**Message**: Theres isnt a day where @115948 dont kill me with frustration! Cant do the simplest things like.. play music! Without skipping tracks!
- **Gold**: Software Bug / Glitch
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: True
- **Notes**: "Music playback failure is specific

### GOLDEN_016
**Message**: @AppleSupport is it just me, or are there issues with iTunes the last few days?  Mine keeps freezing up...  No update available.
- **Gold**: Software Bug / Glitch
- **Predicted**: Services & Account
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_018
**Message**: I want ios 10 back on my device how can i get that plz help me @115858 the Battery life is worse than i expected i m using 6s
- **Gold**: How-To / Feature Question
- **Predicted**: Device Performance / Hardware
- **Ambiguous**: True
- **Notes**: "Primarily asks how to downgrade iOS

### GOLDEN_019
**Message**: @AppleSupport literally cannot figure out how to delete a movie off my phone for the life of me since the new update.
- **Gold**: How-To / Feature Question
- **Predicted**: Software Bug / Glitch
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_021
**Message**: I upgraded my phone to iOS11. I had 3GB of storage free. Business as usual and now I am out of storage space. What gives? @AppleSupport
- **Gold**: Device Performance / Hardware
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: True
- **Notes**: Storage loss after update could be software behavior or storage management; needs human review.

### GOLDEN_022
**Message**: @AppleSupport um hi my iphone SE keeps restarting. It's been doing it all day and I have no idea why. Can you provide any advice? Thanks.
- **Gold**: Device Performance / Hardware
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_025
**Message**: @AppleSupport y’all got me fucked up my X be blacking out and hanging up calls on FaceTime out of no where
- **Gold**: Software Bug / Glitch
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_026
**Message**: @AppleSupport what's happening to my computer? https\\://t.co/HoqpCrRejO
- **Gold**: Device Performance / Hardware
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: True
- **Notes**: Message is too vague and relies on an attached image/context not present here.

### GOLDEN_031
**Message**: I updated my phone &amp; I'm still seeing ? boxes @AppleSupport https\\://t.co/MFe5qaGuVT
- **Gold**: Software Bug / Glitch
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_034
**Message**: thanks for the new iphone update @115858 my fav feature is how my phone freezes up on me like five times a day
- **Gold**: Device Performance / Hardware
- **Predicted**: Software Bug / Glitch
- **Ambiguous**: False
- **Notes**: nan

### GOLDEN_035
**Message**: @115858 @AppleSupport My new #iPhoneX shows a green line on it’s display just on it’s third day! HELP OUT https\\://t.co/cTtbFTyaaX
- **Gold**: Device Performance / Hardware
- **Predicted**: General Complaint / Venting (Other)
- **Ambiguous**: False
- **Notes**: nan
