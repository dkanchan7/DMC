Code Tour:
1. Import Party:
We kick off the script by bringing in the cool kids-conceptnet_lite, NRCLex, profanity, and openai.

2. Hooking Up with ConceptNet Lite:
We make things official with ConceptNet Lite, connecting like old pals using conceptnet_lite.connect("").

3. Function get_emotion_words:
This function is the word matchmaker. It finds words related to your input and filters them based on a specific emotion. It's like asking ConceptNet for word suggestions and then being picky about the vibes.

4. Function generate_story:
Now, this is where the storytelling magic happens. You give it a prompt, a character, and an emotion, and it fashions a story template. It's like a story Mad Libs - just plug in the blanks for character and emotion.

5. Function get_story:
This function gets a bunch of stories for words related to your input and the specified emotion. It uses the previously mentioned word matchmaker and the storytelling maestro (generate_story).

6. Main Event:
You, the user, get a VIP invitation to enter a word and an emotion. Think of it as the script rolling out the red carpet for you.The script then sprinkles its magic, fetching stories and related emotion words, and proudly displays them on the console.
