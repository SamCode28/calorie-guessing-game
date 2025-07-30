//Game Variables
let correct_answer_btn

//Main Menu Variables
//Main Menu Variables
const main_menu_container = document.getElementById('main-menu-container-id')
const g2_play_button = document.getElementById('play-game-2')

g2_play_button.addEventListener('click', get_food_data_with_id)

//Single Food Game Variables
//Single Food Game Variables
const g1_game_container = document.getElementById("g1-game-container-id")
//Buttons
const g1_answer_btns = [
  document.getElementById("game-1-btn-1"),
  document.getElementById("game-1-btn-2"),
  document.getElementById("game-1-btn-3"),
  document.getElementById("game-1-btn-4")
]
const g1_next_btn = document.getElementById('g1-next-btn-id')
//Pre Guess Displayed Data
const g1_question_setence = document.getElementById('g1-question-sentence-id')
const g1_question_span = document.getElementById('game-one-question-span')
const g1_header_name = document.getElementById("game-one-header-span")
const g1_card_name = document.getElementById("card-1-name")
const g1_food_img = document.getElementById("img-container-1")
//Post Guess Displayed Data
const g1_protein = document.getElementById("card-1-protein")
const g1_carb = document.getElementById("card-1-carb")
const g1_fiber = document.getElementById("card-1-fiber")
const g1_fat = document.getElementById("card-1-fat")
const g1_calories = document.getElementById("card-1-calories")
const g1_post_guess_data_list = [g1_protein, g1_carb, g1_fiber, g1_fat, g1_calories]

//Utility Functions
//Utility Functions
function setDisplayHidden(element){
  element.classList.add('hidden')
}

function removeDisplayHidden(element){
  element.classList.remove('hidden')
}

function setInnerText(id, text){
  document.getElementById(id).innerText = text
}

//Main Menu Functions
//Main Menu Functions

//Transition from main menu to game one
document.getElementById('play-game-1').addEventListener('click', () => {
  hide_main_menu()
  open_g1()
  set_single_food_game_display_data()
  hide_answer_data_single_food_game()
});

function hide_main_menu(){
  setDisplayHidden(main_menu_container)
}

function open_g1(){
  removeDisplayHidden(g1_game_container)
}

//Game One Functions
//Game One Functions

//Game_one_correct_answer and game_one_incorrect_answer is redudant
function g1_answer_button_outcomes(){
  g1_answer_btns.forEach((button) => {
    if(button != correct_answer_btn){
      button.classList.add('incorrect-answer-btn')
    }
    else{
      button.classList.add('correct-answer-btn')
    }
    button.removeEventListener('click', g1_answer_button_outcomes)
  })
  show_answer_data_single_food_game()
  removeDisplayHidden(g1_next_btn)
  setDisplayHidden(g1_question_setence)
}

async function set_single_food_game_display_data(){
  let foodData = await get_food_data_with_id();
  //Pre Guess Data
  g1_question_span.innerText = foodData.food_name
  g1_card_name.innerText = foodData.food_name
  g1_food_img.src = foodData.img_url
  //Post Guess Data
  g1_protein.innerText = foodData.protein
  g1_carb.innerText = foodData.carbs
  g1_fiber.innerText = foodData.fiber
  g1_fat.innerText = foodData.fat
  g1_calories.innerText = foodData.calories
  //Buttons
  randomize_game_one_button_answers(parseInt(foodData.calories))
}

function randomize_game_one_button_answers(correct_answer){
  //Set correct answer to a random button
  correct_answer_btn = g1_answer_btns[Math.floor(Math.random() * 4)]
  correct_answer_btn.addEventListener('click', g1_answer_button_outcomes)
  correct_answer_btn.textContent = correct_answer
  //Set incorrect answers
  answer_modifier_nums = [.25, .5, .75, 1.25, 1.5, 1.75, 2]
  rand_index_of_answer_modifier = Math.floor(Math.random() * 6)
  g1_answer_btns.forEach((buttton) => {
    if(buttton != correct_answer_btn){
      buttton.addEventListener('click', g1_answer_button_outcomes)
      if(rand_index_of_answer_modifier > 6){
        rand_index_of_answer_modifier = 0
      }
      buttton.textContent = Math.floor(correct_answer * answer_modifier_nums[rand_index_of_answer_modifier])
      rand_index_of_answer_modifier += 1
    }
  })
}

function hide_answer_data_single_food_game(){
  g1_post_guess_data_list.forEach((span) => span.classList.add('hidden'));
}

function show_answer_data_single_food_game(){
  g1_post_guess_data_list.forEach((span) => span.classList.remove('hidden'));
}

async function get_food_data_with_search_term(){
  let response = await fetch('/get-food', {
    method: 'GET',
    headers: {"Content-Type" : "application/json"}
  })
  let response_json = await response.json()
  return response_json

  //.catch(error => {
  //  console.error('API error:', error);
  //})
}

async function get_food_data_with_id(){
  let response = await fetch('/get-food-data-with-id', {
    method : "Get",
    headers: {"Content-Type" : "application/json"}
  })
  let response_json = await response.json()
  return response_json
}

function g1_display_next_question(){
  set_single_food_game_display_data()
  hide_answer_data_single_food_game()
  removeDisplayHidden(g1_question_setence)
  setDisplayHidden(g1_next_btn)

  g1_answer_btns.forEach((btn) => {
    if(btn == correct_answer_btn){
      btn.classList.remove('correct-answer-btn')
    }
    else{
      btn.classList.remove('incorrect-answer-btn')
    }
  })
}

g1_next_btn.addEventListener('click', g1_display_next_question)
g2_play_button.addEventListener('click', get_food_data_with_id)