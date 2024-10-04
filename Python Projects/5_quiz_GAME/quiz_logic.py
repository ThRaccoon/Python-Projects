class QuizLogic:
    def __init__(self, q_and_a_list):
        self.counter = 0
        self.guessed_questions = 0
        self.current_question = 0
        self.q_and_a_list = q_and_a_list

    def next_question(self):
        self.counter += 1

    def update_current_question(self):
        self.current_question += 1
        return self.current_question

    def question_text(self):
        question_txt = self.q_and_a_list[self.counter]['question']
        return question_txt

    def check_user_answer(self, user_answer):
        if self.q_and_a_list[self.counter]['answer'] == user_answer:
            self.guessed_questions += 1
            return self.guessed_questions, "Green"
        else:
            return self.guessed_questions, "Red"
