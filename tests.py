import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_multiple_choices():
    question = Question(title='q1', max_selections=3)
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('c', False)
    choice4 = question.add_choice('d', True)
    
    assert len(question.choices) == 4
    assert choice1.text == 'a'
    assert choice2.text == 'b'
    assert choice3.text == 'c'
    assert choice4.text == 'd'
    assert choice2.is_correct is True
    assert choice4.is_correct is True

def test_remove_choice_by_invalid_id():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    valid_id = choice1.id
    
    with pytest.raises(Exception):
        question.remove_choice_by_id('fsdfds')
        
    question.remove_choice_by_id(valid_id)
    assert len(question.choices) == 0

def test_select_choices_valid_and_invalid_ids():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('b', False)
    
    selected = question.select_choices([choice1.id, choice2.id])
    assert len(selected) == 2
    assert choice1.id in selected
    assert choice2.id in selected
    
    with pytest.raises(Exception):
        question.select_choices([choice1.id, 'fSDFSDf'])

def test_set_multiple_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', False)
    
    question.set_correct_choices([choice1.id, choice2.id])
    
    assert choice1.is_correct is True
    assert choice2.is_correct is True
    assert choice3.is_correct is False

def test_max_selections_limit_exceeded():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('c', False)
    
    with pytest.raises(Exception):
        question.select_choices([choice1.id, choice2.id, choice3.id])

def test_question_creation_with_negative_points():
    with pytest.raises(Exception):
        Question(title='q1', points=-1)

def test_question_creation_with_points_out_of_range():
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_choice_with_special_characters_in_text():
    question = Question(title='q1')
    
    choice = question.add_choice('@#!$', False)
    assert choice.text == '@#!$'

def test_choice_id_is_unique_across_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    
    choice1 = question1.add_choice('a', False)
    choice2 = question2.add_choice('a', False)
    
    assert choice1.id != choice2.id

def test_invalid_choice_removal_due_to_empty_choice_list():
    question = Question(title='q1')
    
    with pytest.raises(Exception):
        question.remove_choice_by_id('non_existing_id')
