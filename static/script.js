class BoggleGame{
    constructor(seconds = 60){
        this.secondsLeft = seconds;
        this.score = 0;
        this.canGuess = true;
        this.wordsFound = new Set();
        this.minuteTimer = setInterval(this.handleSecond.bind(this), 1000);
        $("form").on("submit", this.handleSubmit.bind(this));
    
    }
    //Adds word to list of found words (after word is found)
    addFoundWord(foundWord){
        $(".words-found").append($("<li>", { text: foundWord }));
    }
    //Updates score (after word is found*)
    updateScore(score){
        $(".score b").text(score);
    }
    updateSeconds(secondsLeft){
        $(".seconds-left b").text(secondsLeft);
    }

    async handleSubmit(e){
        e.preventDefault();

    if(this.canGuess){
        const guess = $(".guess").val(); // Use .val() to get the input value
        
        //invalid word
        if (!guess){
            return;
        }

        //if word was already found
        if(this.wordsFound.has(guess)){
            $(".message").text("Word already found");
            return
        }
        
        //sends guess to server
        let response = await axios.get('/check-guess', { params:{ "guess": guess }});
        let result = response.data.result;

        //if result is good, update score
        if (result == "ok"){
            this.score += guess.length;
            this.addFoundWord(guess); 
            this.wordsFound.add(guess);
            this.updateScore(this.score);
            console.log(this.score);
        }
        //sets message to the result
        $(".message").text(result);
    }
    //resets input
    $(".guess").val("");

    }


    async handleSecond(){
        if (this.secondsLeft > 0){
            this.secondsLeft -= 1;
            this.updateSeconds(this.secondsLeft);
            console.log(this.secondsLeft);
        }
        else{
            clearInterval(this.minuteTimer);
            console.log("Times up!");
            this.canGuess = false;
            
            let response = await axios.post("/post-score",  {"score": this.score});
            console.log(response.data);
        }
        
    }
}

let game = new BoggleGame(60);