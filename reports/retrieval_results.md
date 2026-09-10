# Historical Evidence Retrieval Report

## Methodology

- **Retriever**: Deterministic TF-IDF + Cosine Similarity (Baseline)
- **Leakage Prevention**: Exclusion by `conversation_id` enforced during search.
- **Proxy Relevance Metric**: Percentage of queries where at least one retrieved result's customer message yields the same baseline-classified intent as the gold query. *(Note: This is a proxy measurement, not a genuine human relevance judgment.)*

## Detailed Inspections

## Summary Metrics

- **Queries Processed**: 200
- **Queries with ≥1 Result**: 200 (100.0%)
- **Average Top-K Similarity**: 0.4961
- **Proxy Relevance Hit Rate**: 69.0%

Showing retrieval inspections for the first 20 examples:

### Query: GOLDEN_001
**Customer Message**: @AppleSupport how long until you fix the keyboard issues with the autocorrecting of letters?
**Gold Intent**: Software Bug / Glitch
  - **Result 1** (Sim: 0.499, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport so why is “i” autocorrecting???
    - Resolution: @454673 We'd like to hear more about what's going on. Please DM us about this issue and we'll continue there. https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.491, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @115858    Fix my letters on my iPhone 6 please 😭😭 @AppleSupport  @115858
    - Resolution: @481416 Hi. We are here to help. What issue are you having with the keyboard?
  - **Result 3** (Sim: 0.483, Proxy Intent: General Complaint / Venting (Other))
    - Issue: And once again, @115858 FIX THIS SHIT WITH THE LETTERS
    - Resolution: @719522 We know how inconvenient it can be to have to fix autocorrect issues. We can help. Backup and update your iPhone as our article explains: https://t.co/80YRnjDFDk Once you're on iOS 11.1.1, DM us if you still have any issues. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.476, Proxy Intent: Software Bug / Glitch)
    - Issue: @115858 how long is it going to take for y’all to fix this “I️” keyboard issue?
    - Resolution: @461654 Let's work on this together in DM. Follow us there using the link below: https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.473, Proxy Intent: Software Bug / Glitch)
    - Issue: @115858 so is there an update coming to fix the keyboard? Some letters don’t work.
    - Resolution: @462924 We'd love to talk to you about this. Let's go into DM. https://t.co/GDrqU22YpT


### Query: GOLDEN_002
**Customer Message**: @AppleSupport you seem to be skipping the step that allows to select which carrier phone to get for iPhone X upgrade head start. Why?
**Gold Intent**: Purchase & Store Operations
  - **Result 1** (Sim: 0.400, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport trying to get a head start on my iPhone X upgrade and I can’t connect to the server? https://t.co/qkEmEyKCis
    - Resolution: @387014 We'll be happy to assist as best we can. At what point are you seeing this happen? Let us know in DM and we'll continue there. https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.329, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport I've been trying to get my "head start" upgrading to iPhone X on the iPhone Upgrade Program, but no luck. Help/tips?
    - Resolution: @376369 Anytime! Let us know if we can be of further assistance. Take care.
  - **Result 3** (Sim: 0.295, Proxy Intent: Purchase & Store Operations)
    - Issue: @AppleSupport frustrated, went to Apple store to upgrade the phone, system was down, had to head back home with old phone :(
    - Resolution: @701811 We’d like to know more about your experience. Meet us over in DM with some more details about what happened, and we’ll take a look at this together. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.290, Proxy Intent: How-To / Feature Question)
    - Issue: @AppleSupport how do I begin the head start on pre-ordering the iPhone X?
    - Resolution: @179287 For help with answering your preordering questions, connect with our Apple Online Store support here: https://t.co/8yjRd1Xo0i
  - **Result 5** (Sim: 0.279, Proxy Intent: Software Bug / Glitch)
    - Issue: @AppleSupport I keep getting this error on the iPhone Upgrade Program pre-approval process Confirm Carrier step. Is it a Verizon issue? https://t.co/RL3uVETAKl
    - Resolution: @4872 Hey there! As the message says there is a problem reaching the carrier's server, you'll want to reach out to your carrier for help.


### Query: GOLDEN_003
**Customer Message**: Bruhhhh I’m so fuckin tired @AppleSupport @115858 fixed these damn glitches ! Keep cutting my phone off
**Gold Intent**: Device Performance / Hardware
  - **Result 1** (Sim: 0.364, Proxy Intent: Software Bug / Glitch)
    - Issue: If my iPhone glitches out one more time because of this damn update.... 👿🙄😾 @115858
    - Resolution: @497969 We'd like to help. Please let us know in DM if you're experiencing this while using a particular app. https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.353, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @115858 can u fix me fuckin I️
    - Resolution: @518832 Here’s what you can do to work around the issue until it’s fixed in a future software update: https://t.co/xXaXeeSRt9
  - **Result 3** (Sim: 0.339, Proxy Intent: Software Bug / Glitch)
    - Issue: i’m about tired for this damn glitch! Fix it @115858 !
    - Resolution: @630530 We'd be happy to help. DM us and we'll get started. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.330, Proxy Intent: General Complaint / Venting (Other))
    - Issue: what’s up with these glitches @AppleSupport
    - Resolution: @485377 We'd like to get to the bottom of the issue you're seeing. Could you join us in DM with more details? https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.328, Proxy Intent: General Complaint / Venting (Other))
    - Issue: Yo @115858 why are u fuckin my phone up?
    - Resolution: @559824 That's not expected. We'd like to know more to assist. Send us a DM using the link below and we'll continue. https://t.co/GDrqU22YpT


### Query: GOLDEN_004
**Customer Message**: What is this “A” and  QUESTION MARK THAT MY PHONE KEEPS DOING!! @115858 @AppleSupport
**Gold Intent**: Software Bug / Glitch
  - **Result 1** (Sim: 0.699, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport I️ have a question!!! Why is my phone doing this https://t.co/l6PlHngUMg
    - Resolution: @586925 Let's get this resolved and the keyboard working as normal. DM us the version of iOS you're using and we can go from there. https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.691, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @115858 @AppleSupport what’s up with all the question mark Jawns?
    - Resolution: @480275 Tell us a bit more about what you're seeing, and the device you're using in DM. We'd love to help! https://t.co/GDrqU22YpT
  - **Result 3** (Sim: 0.660, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @115858 you need to fix the ‘ I️ ‘ from doing that box with the question mark.
    - Resolution: @515742 Here’s what you can do to work around the issue until it’s fixed in a future software update: https://t.co/xXaXeeSRt9
  - **Result 4** (Sim: 0.645, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @115858 why my phone doing this question mark thing? I’m all the way updated https://t.co/RWVXjTK8nN
    - Resolution: @456845 Let's take a look into this together. Reach out to us in a DM to get started. https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.632, Proxy Intent: General Complaint / Venting (Other))
    - Issue: My phone was doing the question mark thing before I even updated so what’s really going on? @115858
    - Resolution: @599530 Thanks for reaching out. We have a workaround for this here: https://t.co/xXaXeeSRt9 DM us if you still need help. https://t.co/GDrqU22YpT


### Query: GOLDEN_005
**Customer Message**: @AppleSupport any way to actually talk to a store? I've tried 0117 959 7600 (Bristol) and just end up back with AppleCare or Sales each time
**Gold Intent**: Purchase & Store Operations
  - **Result 1** (Sim: 0.328, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport applecare????? https://t.co/PdeQPICKDJ
    - Resolution: @572979 We're happy to help via Twitter however we can. Let us know in DM what's going on and we'll go from there. https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.327, Proxy Intent: Purchase & Store Operations)
    - Issue: @AppleSupport Just bought AppleCare for MacBook, what is difference between AppleCare and AppleCare+?
    - Resolution: @154191 Great question! The main difference is that AppleCare+ isn't available everywhere. This link has more info: https://t.co/brpZQUaYqu
  - **Result 3** (Sim: 0.284, Proxy Intent: General Complaint / Venting (Other))
    - Issue: Is it just me or my current iPhone got slower, stupider and annoying after the new #iPhoneX release! Coincidence or sales move!? #apple @AppleSupport #sales https://t.co/2qmR4UXCu9
    - Resolution: @486293  That is certainly not the experience that we wanted you to have with your device, and we are going to do everything we can to help you. When you have a free moment, can you please DM us which version of iOS you are currently running? https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.281, Proxy Intent: Services & Account)
    - Issue: @AppleSupport I've tried iTunes, I've tried everything https://t.co/XdkUGRtzc3
    - Resolution: @430735 Thanks for image. Send us a DM, and we'll provide further guidance. https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.268, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport please fix this I️ just want to talk about myself https://t.co/nu26NpAFew
    - Resolution: @481032 We're happy to help out. Let's take a look at this further for you. Reach out to us in DM. https://t.co/GDrqU2kzhr


### Query: GOLDEN_006
**Customer Message**: WHY IS THE LETTER I SHOWING UP AS A QUESTION MARK IN A BOX ? @115858 FIX IT
**Gold Intent**: Software Bug / Glitch
  - **Result 1** (Sim: 0.907, Proxy Intent: General Complaint / Venting (Other))
    - Issue: so @115858 the letter “I” is still showing as a box &amp; question mark , wasshpoppin?
    - Resolution: @456038 We're here to help. Please DM us which iOS software version you are using and we'll go from there. https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.841, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport then why are my I️ showing up as a question mark and a A with a box around it. I️ 🤬🤬🤬🤮 I️ https://t.co/eS9ZMYuaKA
    - Resolution: @531804 Hello. Here’s what you can do to work around the issue until it’s fixed in a future software update: https://t.co/uQeXsrrlXJ
  - **Result 3** (Sim: 0.817, Proxy Intent: General Complaint / Venting (Other))
    - Issue: Wtf @115858? Why are my i’s showing up as a question mark in a box!?
    - Resolution: @518237 Here’s what you can do to work around the issue until it’s fixed in a future software update: https://t.co/xXaXeeSRt9
  - **Result 4** (Sim: 0.796, Proxy Intent: Software Bug / Glitch)
    - Issue: @115858 can you fix this glitch on iPhones so I️ can type the letter I️ without it showing up as an A and a box with a question mark
    - Resolution: @505659 Here’s what you can do to work around the issue until it’s fixed in a future software update: https://t.co/xXaXeeSRt9
  - **Result 5** (Sim: 0.772, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @115858 yo I️ can’t type I️ without a question mark box showing up, fix it
    - Resolution: @592621 Let's meet up in DM to discuss this further. On what model device and software version are you seeing this? https://t.co/GDrqU22YpT


### Query: GOLDEN_007
**Customer Message**: @AppleSupport trying to setup HomeKit automation for when multiple people leave home but it says to upgrade my hub -an Apple TV w tvOS 11.1 https\\://t.co/IXpgmAi9vc
**Gold Intent**: How-To / Feature Question
  - **Result 1** (Sim: 0.525, Proxy Intent: Software Bug / Glitch)
    - Issue: Which home hub do i have to update? 🤔 @AppleSupport #HomeKit https://t.co/bHSGrpyiHb
    - Resolution: @442678 We'd like to look into this with you. Have you had the opportunity to try out Home prior to installing beta versions?
  - **Result 2** (Sim: 0.455, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport Will homepod be able to be setup as a "home hub," like ipad and apple tv, or will I need one of those other devices to do automation. This sounds like it is: "And it’s a hub for controlling your smart home accessories." But I'd like confirmation on interpretation.
    - Resolution: @703367 Great question! We appreciate your interest in using HomePod as your home's hub. We encourage you to stay up-to-date on Apple news about HomePod here: https://t.co/gbIPLOsnZd  DM us with any other questions. https://t.co/GDrqU22YpT
  - **Result 3** (Sim: 0.341, Proxy Intent: How-To / Feature Question)
    - Issue: @AppleSupport Can I use my iPad 2 as Domestic Hub for Homekit?
    - Resolution: @149709 The Home app will allow you to control your Homekit accessories. You can learn more about it here: https://t.co/ept6Vf2rqU
  - **Result 4** (Sim: 0.341, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @104870 @AppleSupport Hi, is it possible to link my Hive lights/hub to Apple HomeKit?
    - Resolution: @801248 Hi! To see a list of accessories that work with Apple HomeKit, click here: https://t.co/5OAsDC2ye7
  - **Result 5** (Sim: 0.333, Proxy Intent: Device Performance / Hardware)
    - Issue: @115858 @AppleSupport you guys broke HomeKit on TV with tvOS 11. Routines don't work and my poor dog is sitting in the dark.@213609
    - Resolution: @118301 We'd love to help. Please reach out to our Apple TV specialist for further assistance here: https://t.co/IBIY3w3RGR


### Query: GOLDEN_008
**Customer Message**: Love how my $1200 @115858 iPhone X constantly freezes when using apps like YouTube and Apple Music. Wtf
**Gold Intent**: Device Performance / Hardware
  - **Result 1** (Sim: 0.402, Proxy Intent: General Complaint / Venting (Other))
    - Issue: I️ love this @115858 #wtf #I️
    - Resolution: @594248 We'll be happy to help. To start, take a look at this article: https://t.co/xXaXeeSRt9  DM us if the issue persists. https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.386, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport updated my phone. Now it constantly freezes and apps constantly crash. PLEASE FIX
    - Resolution: @187943 We’d be happy to look into this for you. Send us a DM with the iPhone you are using and the iOS version it is running. https://t.co/GDrqU22YpT
  - **Result 3** (Sim: 0.384, Proxy Intent: General Complaint / Venting (Other))
    - Issue: i️ love music. i️ love music. i️ love music. i️ love music. i️ love music. i️ love music. i️ love music. i️ love music. i️ love music. i️ lo
    - Resolution: @509927 Here’s what you can do to work around the issue until it’s fixed in a future software update: https://t.co/xXaXeeSRt9
  - **Result 4** (Sim: 0.377, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport £1200 for an iPhone X that freezes! Perfect support from apple care! Fed up
    - Resolution: @264196 We'd like to help. Let's take this to DM and we'll explore ways to provide you assistance. https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.361, Proxy Intent: Software Bug / Glitch)
    - Issue: @AppleSupport ever since your update. My phone freezes constantly opening apps!
    - Resolution: @610150 Hey, we want to hear more about what's going on so that we can help you. Let's meet in DM and we'll go from there. https://t.co/GDrqU22YpT


### Query: GOLDEN_009
**Customer Message**: Aye @115858 y’all are gonna need to send another update. Every time I️ type an “I️” it ends up looking like this 😒 https\\://t.co/zqG2JxPR3V
**Gold Intent**: Software Bug / Glitch
  - **Result 1** (Sim: 0.519, Proxy Intent: General Complaint / Venting (Other))
    - Issue: How come every time I type “it” it ends up being”I.T “ ? @AppleSupport
    - Resolution: @240819 We'd love to look into this concern with you further. Meet us in DM to continue please: https://t.co/GDrqU2kzhr
  - **Result 2** (Sim: 0.491, Proxy Intent: Software Bug / Glitch)
    - Issue: Aye @AppleSupport y’all need to fix this update I️ want to type I not I️
    - Resolution: @461861 We're here to help. DM us which iOS version you're on. https://t.co/GDrqU22YpT
  - **Result 3** (Sim: 0.456, Proxy Intent: General Complaint / Venting (Other))
    - Issue: Why is my I️ looking like this @115858 @AppleSupport https://t.co/EmX0GJRfaL
    - Resolution: @484905 We’re here for you. Try the steps here and let us know if you still need help: https://t.co/xU1AGHStV6
  - **Result 4** (Sim: 0.425, Proxy Intent: Software Bug / Glitch)
    - Issue: @115858 aye y’all need to fix this “ I️ “ issue
    - Resolution: @269726 Have you checked your phone for a software update recently? You'll want to do that to install the fix. Let us know if this helps! https://t.co/80YRnjDFDk
  - **Result 5** (Sim: 0.419, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport  why are my “I️” looking like this....
    - Resolution: @510106 Here’s what you can do to work around the issue until it’s fixed in a future software update: https://t.co/xXaXeeSRt9


### Query: GOLDEN_010
**Customer Message**: @AppleSupport with iOS11 my phone won’t show my music on my lock screen and when I receive calls I can’t hear anything on the other end help
**Gold Intent**: Software Bug / Glitch
  - **Result 1** (Sim: 0.616, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport my phone can make calls but I can’t hear anything at the other end?!
    - Resolution: @753808 Thanks for reaching out. Let us know if this helps: https://t.co/XlmCP2gCtj
  - **Result 2** (Sim: 0.577, Proxy Intent: General Complaint / Venting (Other))
    - Issue: Why do my calls end immediately? I can’t call or receive calls @115858 @AppleSupport help please
    - Resolution: @718410 Thank you for reaching out. We're here to help. To get started, let's go into Settings &gt; General &gt; About. If you are prompted for a carrier update, please apply and restart. Then test to see if you are able to make outgoing calls. We look forward to your reply.
  - **Result 3** (Sim: 0.546, Proxy Intent: Device Performance / Hardware)
    - Issue: Why won’t my music show up on my lock screen 🙃🙃🙃 @115858
    - Resolution: @391261 That is not the experience we want you to have. We are here to help. What kind of device are you using?
  - **Result 4** (Sim: 0.519, Proxy Intent: Software Bug / Glitch)
    - Issue: @AppleSupport updated to iOS 11.3 and now when I receive or make calls I cannot hear &amp; they cannot hear me?! Help 😭😭 #wpple #ios11update
    - Resolution: @120959 Communication is key! We want you to be able to make and receive those calls. Does restarting your device help at all?
  - **Result 5** (Sim: 0.503, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport can’t call anyone or receive calls 🙄
    - Resolution: @718005 Check out this article for steps to take if you not able to make or receive calls: https://t.co/U53YusKX3z


### Query: GOLDEN_011
**Customer Message**: @AppleSupport  I updated to iOS 11.0.3 on my 6s plus &amp; I just went from 85% to 13% in an hour after watching two YouTube videos. :/
**Gold Intent**: Device Performance / Hardware
  - **Result 1** (Sim: 0.410, Proxy Intent: General Complaint / Venting (Other))
    - Issue: My phone been at 85% for a hour @AppleSupport wassup?
    - Resolution: @590744 Hey there! We'd be happy to look into this with you, but we'll need some background first. Shoot us a DM and we'll go from there. https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.389, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport Why does sometimes Hey siri go off when i am watching Youtube?
    - Resolution: @221765 Thanks for reaching out. If you're noticing Siri is being triggered accidentally, we'd recommend setting it up again. Check here for more info: https://t.co/vDsPkLKaYM
  - **Result 3** (Sim: 0.385, Proxy Intent: Device Performance / Hardware)
    - Issue: iOS update 11.1.2 is draining my 7 plus battery like crazy. Went to bed at 85%, woke up at 11%. @115858 @AppleSupport
    - Resolution: @287539 We'd be happy to look into this with you more in detail. Please reach out to us via DM and we'll get started. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.381, Proxy Intent: How-To / Feature Question)
    - Issue: @AppleSupport how can I turn off this notification I get when I’m watching YouTube on my phone? https://t.co/dKuQMI876X
    - Resolution: @601959 To hide "Now Playing" take a look at the steps in this article: https://t.co/kPrTOa0hgP If you need more help, DM us! https://t.co/GDrqU2kzhr
  - **Result 5** (Sim: 0.360, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport 5% battery consumed in 13 minutes watching YouTube. Can we expect a fix soon. I have an iPhone 7 on 11.2 beta 2 https://t.co/ZS38nWDt0Y
    - Resolution: @666180 We would love to join together and look into the battery concerns. Join us in DM using this link to get started: https://t.co/GDrqU22YpT


### Query: GOLDEN_012
**Customer Message**: @AppleSupport Since updating to iOS 11 I’m not receiving text alerts on my watch now yet I receive them for WhatsApp &amp; calls 😤
**Gold Intent**: Software Bug / Glitch
  - **Result 1** (Sim: 0.460, Proxy Intent: Software Bug / Glitch)
    - Issue: @AppleSupport since last IOS 11.0.3 I don’t receive Whatsapp notifications
    - Resolution: @335480 We want to help.  If you go to Settings &gt; Notifications &gt; WhatsApp, are notifications turned on?
  - **Result 2** (Sim: 0.457, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport can’t call anyone or receive calls 🙄
    - Resolution: @718005 Check out this article for steps to take if you not able to make or receive calls: https://t.co/U53YusKX3z
  - **Result 3** (Sim: 0.431, Proxy Intent: Software Bug / Glitch)
    - Issue: @4305 @AppleSupport not receiving WhatsApp notifications since latest iOS 11.2 / whatsapp update ? Have tried everything
    - Resolution: @614823 We know how important getting notifications are to using the iPhone. Please let us know if you’ve tried change them via DM. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.400, Proxy Intent: Software Bug / Glitch)
    - Issue: @115858 I can’t make or receive calls ever since I updated to iOS 11. How do I fix that???
    - Resolution: @716995 Thanks for contacting us. We know it's important to stay in touch. We'd like to help out. Let's start with the steps here: https://t.co/U53YusKX3z Please reach out to us in DM if you need further help after trying the steps listed. https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.381, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport Frequently not receiving Whatsapp notifications.. Using 11.0.3
    - Resolution: @312390 We're here for you. Check out "If you don't see notifications" for steps to help in this article: https://t.co/E7sMv2aXe6


### Query: GOLDEN_013
**Customer Message**: @AppleSupport my iPhone 7 Plus keeps freezing, please send help
**Gold Intent**: Device Performance / Hardware
  - **Result 1** (Sim: 0.828, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport my iPhone 7 Plus keeps freezing after update! HELP!!
    - Resolution: @403735 We'd love to work together on this with you. Meet us in DM with additional details to get started: https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.663, Proxy Intent: Device Performance / Hardware)
    - Issue: My iPhone keeps freezing @AppleSupport
    - Resolution: @491465 Let's work on that together. Meet us in DM with your iPhone model and iOS version so we may continue. https://t.co/GDrqU22YpT
  - **Result 3** (Sim: 0.653, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport this update sucks. My iPhone 7 PLUS keeps freezing because of it.
    - Resolution: @204468 Let's see what we can do to help. Send us a DM and we can look into this for you. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.612, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport @569726 iPhone keeps freezing on 11.0.3
    - Resolution: @162992 Thanks for reaching out! Let us know if restarting the iPhone helps in DM. We’ll continue troubleshooting there. https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.597, Proxy Intent: Device Performance / Hardware)
    - Issue: Why does my iPhone 7 Plus keep freezing? @AppleSupport
    - Resolution: @157887 We'd be happy to take a look into this with you. Could you please send us a DM with what iOS version you're running so we can get started? https://t.co/GDrqU22YpT


### Query: GOLDEN_014
**Customer Message**: @AppleSupport Any idea when the @ATT activation servers will stop shitting themselves, or do I keep mashing Try Again &amp; hope? #iphoneXlaunch
**Gold Intent**: Purchase & Store Operations
  - **Result 1** (Sim: 0.385, Proxy Intent: Services & Account)
    - Issue: @AppleSupport I’ve  been trying for two hours and the iTunes activation doesn’t work either 😡  #iphoneXlaunch https://t.co/23lICKNtSM
    - Resolution: @458611 We can help. Try following these steps and DM us if you still have issues: https://t.co/Mhw9pFAK08 https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.381, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @115858 Hey. Any idea when your activation servers are going to be back up? Pretty bummed.
    - Resolution: @476190 We are here to help. DM us the details of your issue and we can take a look at this. https://t.co/GDrqU22YpT
  - **Result 3** (Sim: 0.365, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @applesupport “could not activate iPhone” tried maybe 50 times now.  Any idea when activation servers will work?
    - Resolution: @5107 We'd like to look into this with you. Send us a DM to get started. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.356, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport @115858 @ATT What is the problem with the iPhone Activation Servers??? 3 hours trying hundreds of times and still unsuccessful!
    - Resolution: @592497  We're eager to get your iPhone activated. Send a DM, and we'll check into this concern with your Activation. https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.349, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @applesupport iPhone X won't activate cause activation servers are down :( #activationgate
    - Resolution: @592234 Please complete the steps shown in the following article, and DM us if you still cannot active it: https://t.co/ywHIZGN4Ac https://t.co/GDrqU22YpT


### Query: GOLDEN_015
**Customer Message**: Theres isnt a day where @115948 dont kill me with frustration! Cant do the simplest things like.. play music! Without skipping tracks!
**Gold Intent**: Software Bug / Glitch
  - **Result 1** (Sim: 0.301, Proxy Intent: How-To / Feature Question)
    - Issue: Hi @AppleSupport! Why is Apple Music randomly stops playing "not downloaded" tracks and skipping to the next song? How can i fix it?
    - Resolution: @258648 We want to help.  Does this happen on more than one device?  Does it happen both when you are connected to Bluetooth and Wi-Fi?
  - **Result 2** (Sim: 0.286, Proxy Intent: Software Bug / Glitch)
    - Issue: @AppleSupport i want to fucking kill myself why cant I play my music anymore with this new Ios update
    - Resolution: @623046 This is unexpected. We're here to help. Meet us in DM and we'll take a further look at this with you. https://t.co/GDrqU22YpT
  - **Result 3** (Sim: 0.282, Proxy Intent: General Complaint / Venting (Other))
    - Issue: There’s games, then theres this shit #HeartbreakOnAFullMoon @115858 @115948 @AppleSupport https://t.co/ZBXA4O656G
    - Resolution: @454899 We'd like to continue working with you on this. Let's go back to DM and team up to get it resolved. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.270, Proxy Intent: General Complaint / Venting (Other))
    - Issue: Wahhh I can't play starboy by @3523 please fix your @115948 !!!!! @115858 https://t.co/Vq5GjkZCVW
    - Resolution: @561855 Which iOS is installed? You can check in Settings &gt; General &gt; About. Send us a DM and let us know, please. https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.260, Proxy Intent: General Complaint / Venting (Other))
    - Issue: My phone won't play anything bc it says there's headphones plugged in BUT THERES NOT WHY DOES MY PHONE RANDOMLY DO WEIRD THINGS @115858
    - Resolution: @565899 We want to help! What model of iOS device are you using? Do you have the most recent version of iOS 11.0.3 downloaded? https://t.co/GDrqU22YpT


### Query: GOLDEN_016
**Customer Message**: @AppleSupport is it just me, or are there issues with iTunes the last few days?  Mine keeps freezing up...  No update available.
**Gold Intent**: Software Bug / Glitch
  - **Result 1** (Sim: 0.504, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport this update keeps freezing my phone!
    - Resolution: @451640 We're happy to assist. Which iOS 11 version are you currently running? Go to Settings &gt; General &gt; About for the version.
  - **Result 2** (Sim: 0.485, Proxy Intent: Device Performance / Hardware)
    - Issue: Anyone else have issues with their iPhone after the iOS #update? Mine keeps freezing. #frustrating @115858 @AppleSupport
    - Resolution: @698844 We want to help. Reach out via DM using the link below. https://t.co/GDrqU22YpT
  - **Result 3** (Sim: 0.460, Proxy Intent: Device Performance / Hardware)
    - Issue: My iPhone keeps freezing @AppleSupport
    - Resolution: @491465 Let's work on that together. Meet us in DM with your iPhone model and iOS version so we may continue. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.452, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport  I have had to restart my iPhone about 10 times in the last 2 days, it  just keeps freezing ever since i updated to 11.0.3??
    - Resolution: @574237 That's not the experience we want you to have. DM us which iPhone you're using to get started. https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.450, Proxy Intent: Software Bug / Glitch)
    - Issue: When the update will be available?  iOS 11.1 @AppleSupport.
    - Resolution: @123833 iOS 11.1 is available now. You can update using the steps here: https://t.co/80YRnjDFDk


### Query: GOLDEN_017
**Customer Message**: @AppleSupport what password is this referring to? It will not accept my iCloud, computer, or phone password https\\://t.co/tcZVKRuynn
**Gold Intent**: Services & Account
  - **Result 1** (Sim: 0.692, Proxy Intent: Services & Account)
    - Issue: When @115858 makes you change your computer password, but then won't accept your computer password, and then requires that password it won't accept to CHANGE your password. #wtf
    - Resolution: @774810 Let us know if you're still having trouble with your computer password because we'll be happy to check it out with you. To start, DM us some more info about what's going on. https://t.co/GDrqU22YpT
  - **Result 2** (Sim: 0.486, Proxy Intent: Services & Account)
    - Issue: @AppleSupport after iOS update iCloud does not accept new password, after having to re-der it again (!) cannot sign out on phone.
    - Resolution: @402422 We can definitely look into this with you. What's the error that you see when you attempt to sign out of your account?
  - **Result 3** (Sim: 0.485, Proxy Intent: Services & Account)
    - Issue: Why doesn't @115858 work like they used to? I get a random charge and I'm trying to access my account but it won't accept my password...so i change it.. and it won't accept that password either.. No help from their call in number either..
    - Resolution: @135260 We'd be happy to look into this with you more in detail. Please reach out to us via DM and we'll get started. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.457, Proxy Intent: Services & Account)
    - Issue: @applesupport hi, trying to restore back up on to new phone, asking for password to unlock back up but iTunes password or phone password isn’t working. Any ideas?
    - Resolution: @230654 We want to do all that we can to help you get your data back onto the iPhone. To clarify, are you trying to restore from an iTunes backup? If so, it sounds like it may be an encryption password. Take a look here for more info: https://t.co/s6tdVStcb2
  - **Result 5** (Sim: 0.446, Proxy Intent: Services & Account)
    - Issue: @AppleSupport my password is not working! Just now!
    - Resolution: @797554 We would be glad to help. Are you having issues with your Apple ID password? Let us know in DM. https://t.co/GDrqU22YpT


### Query: GOLDEN_018
**Customer Message**: I want ios 10 back on my device how can i get that plz help me @115858 the Battery life is worse than i expected i m using 6s
**Gold Intent**: How-To / Feature Question
  - **Result 1** (Sim: 0.438, Proxy Intent: Device Performance / Hardware)
    - Issue: My battery life is worse than it's ever been @AppleSupport #update
    - Resolution: @379765 Let's get the most out of your battery. Which model do you have and is iOS 11.0.3 the version installed? Any steps tried?
  - **Result 2** (Sim: 0.436, Proxy Intent: Purchase & Store Operations)
    - Issue: @115858 @AppleSupport Unable to download or update apps from App Store...Facing too many problem after updating my device iOS 11,was happy with iOS 10...!! Plz help..!! 🙏🏻  DEVICE : iPhone 6s
    - Resolution: @287016 We're happy to help with downloading your apps. Meet us in DM with more details, such as any errors messages you're getting and which country you're in, and we'll get started. https://t.co/GDrqU22YpT
  - **Result 3** (Sim: 0.419, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport why with every iOS update the battery life is getting worse?
    - Resolution: @740641 We know how important it is to have a working battery. We'll do everything we can to help. Let's take a closer look at what's happening via DM. Tell us what type of iOS device you're using, along with the specific iOS version you currently have installed. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.395, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport iOS 11.0.3 on iPhone 7plus. Battery life is HORRIBLE. Much worse than on iOS 10.x. Fix this!
    - Resolution: @663032 Let us help you get this sorted out. DM us so we can better assist you: https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.390, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport i want to my iPhone battery life
    - Resolution: @219641 We've gotten your DM and will continue working with you there to help with your iPhone battery life.


### Query: GOLDEN_019
**Customer Message**: @AppleSupport literally cannot figure out how to delete a movie off my phone for the life of me since the new update.
**Gold Intent**: How-To / Feature Question
  - **Result 1** (Sim: 0.409, Proxy Intent: How-To / Feature Question)
    - Issue: Now could someone please help me figure out how to #delete #all my #email at once on my #iPhone8 @AppleSupport #apple
    - Resolution: @302077 We're happy to help. From your inbox, you can use the Edit button (top right corner) to select and delete multiple emails at once.
  - **Result 2** (Sim: 0.395, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport literally one hour of battery life with new iOS 11.1🤦🏻‍♂️
    - Resolution: @591614 Hey there, thanks for reaching out! We know how vital the battery is &amp; we'll definitely take a look with you. Please DM us. https://t.co/GDrqU22YpT
  - **Result 3** (Sim: 0.369, Proxy Intent: Software Bug / Glitch)
    - Issue: I literally hate the new @115858 update.
    - Resolution: @424364 Wi-Fi and Bluetooth toggles work a bit differently in iOS 11. This article has more information: https://t.co/vzVz37Hb6q
  - **Result 4** (Sim: 0.369, Proxy Intent: How-To / Feature Question)
    - Issue: What is “other” and how can I delete it? @115858 @AppleSupport https://t.co/edqANKuF0m
    - Resolution: @173313 Thanks for contacting us, we can help you with the “Other” data question. Please check out this “About cached files in "Other" iOS storage” section of this support article: https://t.co/0yFHFRYSnX
  - **Result 5** (Sim: 0.368, Proxy Intent: General Complaint / Venting (Other))
    - Issue: @AppleSupport Figure this shit out already https://t.co/DQMeZIJdM4
    - Resolution: @629741 Here’s what you can do to work around the issue until it’s fixed in a future software update: https://t.co/uQeXsrrlXJ


### Query: GOLDEN_020
**Customer Message**: @AppleSupport ever since I updated my iPhone 6 to iOS 11.1 (currently at 11.1.2) my battery life is terrible.  I lose 10%/hr with the phone locked and in “low power” mode.  Support told me it is a known issue with iOS 11.1 When will it be fixed?
**Gold Intent**: Device Performance / Hardware
  - **Result 1** (Sim: 0.508, Proxy Intent: Device Performance / Hardware)
    - Issue: iOS 11 is great for battery life: NOT! 10% per hour on low power mode. Don’t upgrade.   @115858 its terrible!!
    - Resolution: @664162 We're happy to assist. Which iOS 11 version are you currently running? Go to Settings &gt; General &gt; About for the version.
  - **Result 2** (Sim: 0.468, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport Battery life terrible since downloading IOS 11.1 on my 6S. Even in Low Power mode, battery life dropping 1% every 2 minutes!
    - Resolution: @631302 We've received your DM and we will respond to you in there to help you with your battery. Thanks.
  - **Result 3** (Sim: 0.436, Proxy Intent: Device Performance / Hardware)
    - Issue: @115858 what’s with the battery issues?  iOS 11.1 and I have to keep my phone in low power mode all day. Seriously?
    - Resolution: @477297 We're here for you. DM us using the link below and we'll go from there. https://t.co/GDrqU22YpT
  - **Result 4** (Sim: 0.420, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport just updated to iOS 11.1 from 10.3.3 on an iPhone 6s Plus and the battery life is TERRIBLE please fix!!
    - Resolution: @592413 Let's team up in DM and get this looked into. Meet us there with a few more details, and we'll get started. https://t.co/GDrqU22YpT
  - **Result 5** (Sim: 0.412, Proxy Intent: Device Performance / Hardware)
    - Issue: @AppleSupport   I am currently on the latest iOS 11.1.2 but I am experience a screen issue.. is this a known bug? When ever the phone is locked an I hit the power button this happens Everytime https://t.co/JBwjBDjm2r
    - Resolution: @277635 We'd love to take a look at this with you!  We received your DM so look for our reply there soon! https://t.co/GDrqU22YpT

