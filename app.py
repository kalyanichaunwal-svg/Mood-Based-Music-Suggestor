from flask import Flask, request, jsonify, redirect, render_template 
import json
import random

app = Flask(__name__)


# Load songs data
with open("songs-1.json", "r", encoding="utf-8") as f:
    songs_data = json.load(f)

VALID_MOODS = ["happy", "sad", "calm", "energetic", "romantic", "chill"]
VALID_LANGUAGES = ["hindi", "english"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/language")
def language_page():
    return render_template("language.html")


@app.route("/playlist")
def playlist_page():
    return render_template("playlist.html")


@app.route("/play")
def play_song():
    mood = request.args.get("mood")
    language = request.args.get("language")
    random_play = request.args.get("random")

    # Step 1: Ask for mood if not provided
    if not mood:
        return render_template('''
            <h2>Select a mood:</h2>
            {% for m in moods %}
                <a href="/play?mood={{m}}">{{m.title()}}</a><br>
            {% endfor %}
        ''', moods
    =VALID_MOODS)

    mood = mood.lower()
    if mood not in VALID_MOODS:
        return jsonify({"error": f"Invalid mood '{mood}'", "available_moods": VALID_MOODS}), 400

    # Step 2: Ask for language if not provided
    if not language:
        return render_template('''
            <h2>Mood selected: {{mood.title()}}</h2>
            <p>Select a language:</p>
            {% for lang in languages %}
                <a href="/play?mood={{mood}}&language={{lang}}">{{lang.title()}}</a><br>
            {% endfor %}
        ''', mood=mood, languages=VALID_LANGUAGES)

    language = language.lower()
    if language not in VALID_LANGUAGES:
        return jsonify({"error": f"Invalid language '{language}'", "available_languages": VALID_LANGUAGES}), 400

    # Step 3: Show all songs for selected mood and language
    songs_list = songs_data.get(language, {}).get(mood, [])
    if not songs_list:
        return f"<h3>No songs found for {mood.title()} mood in {language.title()} language.</h3>"

    # If user clicked random button
    if random_play == "true":
        song = random.choice(songs_list)
        return redirect(song["external_url"])
    
    # Otherwise, show song list 
    return render_template('''
        <h2>{{mood.title()}} Songs ({{language.title()}})</h2>
        <button onclick="window.location.href='/play?mood={{mood}}&language={{language}}&random=true'">
            🎵 Play Random Song
        </button>
        <ul>
            {% for song in songs %}
                <li>
                    <strong>{{song.title}}</strong> – {{song.artist}} 
                    [<a href="{{song.external_url}}" target="_blank">Play on Spotify</a>]
                </li>
            {% endfor %}
        </ul>
        <hr>
        <a href="/play">🔙 Start Over</a>
    ''', songs=songs_list, mood=mood, language=language)
    
@app.route("/api/songs")
def api_songs():
    mood = request.args.get("mood")
    language = request.args.get("language")

    if not mood or not language:
        return jsonify({"error": "mood and language are required"}), 400

    mood = mood.lower()
    language = language.lower()

    if mood not in VALID_MOODS:
        return jsonify({"error": f"Invalid mood '{mood}'"}), 400

    if language not in VALID_LANGUAGES:
        return jsonify({"error": f"Invalid language '{language}'"}), 400

    songs_list = songs_data.get(language, {}).get(mood, [])

    return jsonify(songs_list)




if __name__ == "__main__":
    app.run(debug=True)
