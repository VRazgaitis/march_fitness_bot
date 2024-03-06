WALKTHRU VIDEO
https://www.loom.com/share/a4a8954845d9452b98ca63a94eae59ee?sid=600e9fc6-d48c-4018-bab7-33ca128c1ff1

PROJECT MOTIVATION
Each March, I participate in an annual fitness competition among friends. Participants
in the competition are rewarded points for loggin daily workouts, and compete to win more 
points than other competitors. Historically, points tracking has been done using a shared Google sheets document.

Over the years, the scoring, rules, and logistics of the competition have grown more complicated,
with a growing pool of competitors (296 this year). This year, some friends and I built a website that keeps track of points accounting, and displays a feed of activites and leaderboard. The feed is similar to Venmo, and activity logging is similar to Strava, with an intuitive leaderboard. The website can be found here: https://www.march.fit/leaderboard

With around 100 new participants, the admins of the competition found themselves fielding an inconvenint number of questions regarding scoring and rules. For my final project, I decided to build and deploy a Retrieval-Augmented Generation (RAG) chatbot on Streamlit. Rather than bogging down admins with simple questions, competitors can instead query the chatbot to better understand the rules of the competition. 

RAG CHATBOT MODEL
The March fitness rules chatbot was supplied with text documents containing intricacies of rules and scoring from the fitness competition. These text clauses came from onboarding emails, scroing rules described on the webpage, and FAQ's from users. I am planning to continue to supply it with more text data throughout the challenge, as more questions and answers get resolved.   

The chatbot is hosted here: https://mfruleschatbot.streamlit.app/

KEY CHALLENGES
-Manually parsing and cleaning data so that rules and regulations can be correctly comprehended by the LLM 
-Hosting and deploying a Streamlit app. Lots of difficulties navigating Python environmnets and imported packages. Getting the tool to deploy locally is much easier than hosting the chatbot online.
-Providing API key to Streamlit without revealing it on a public GitHub repo