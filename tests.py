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
    # testa se os IDs das escolhas são gerados de forma sequencial
    question = Question(title='Teste de múltiplas escolhas')
    choice1 = question.add_choice('Escolha 1', False)
    choice2 = question.add_choice('Escolha 2', True)
    assert len(question.choices) == 2
    assert choice1.id == 1
    assert choice2.id == 2

def test_remove_choice_by_id():
    # testa o comportamento de remoção de uma escolha pelo seu ID
    question = Question(title='Teste de remoção por ID')
    choice1 = question.add_choice('Escolha 1', False)
    choice2 = question.add_choice('Escolha 2', True)
    question.remove_choice_by_id(choice1.id)
    assert len(question.choices) == 1
    assert question.choices[0].id == choice2.id

def test_remove_choice_by_invalid_id():
    # testa se ao tentar remover uma escolha inexistente é lançada uma exceção
    question = Question(title='Teste de remoção inválida')
    question.add_choice('Escolha 1', False)
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    # testa se o método de remoção de todas as escolhas limpa corretamente a lista
    question = Question(title='Teste de remoção de todas as escolhas')
    question.add_choice('Escolha 1', False)
    question.add_choice('Escolha 2', True)
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_select_choices_exceed_max_selections():
    # garante que selecionar mais escolhas do que permitido gera exceção
    question = Question(title='Teste de seleção excedida', max_selections=1)
    choice1 = question.add_choice('Escolha 1', True)
    choice2 = question.add_choice('Escolha 2', False)
    with pytest.raises(Exception):
        question.select_choices([choice1.id, choice2.id])

def test_select_choices_only_correct_returned():
    # testa se o método de seleção retorna apenas os IDs das escolhas corretas
    question = Question(title='Teste de seleção correta', max_selections=2)
    choice1 = question.add_choice('Escolha 1', True)
    choice2 = question.add_choice('Escolha 2', False)
    selected_ids = question.select_choices([choice1.id, choice2.id])
    # Mesmo tendo selecionado ambas, apenas a escolha correta deve ser retornada
    assert selected_ids == [choice1.id]

def test_set_correct_choices():
    # testa se o método set_correct_choices marca corretamente a(s) escolha(s) informada(s)
    question = Question(title='Teste de marcação de correta', max_selections=2)
    choice1 = question.add_choice('Escolha 1', False)
    choice2 = question.add_choice('Escolha 2', False)
    question.set_correct_choices([choice2.id])
    assert not choice1.is_correct
    assert choice2.is_correct

def test_add_choice_empty_text():
    # testa se adicionar uma escolha com texto vazio gera exceção
    question = Question(title='Teste de texto vazio')
    with pytest.raises(Exception):
        question.add_choice('', False)

def test_add_choice_long_text():
    # testa se adicionar uma escolha com texto maior que 100 caracteres gera exceção
    question = Question(title='Teste de texto longo')
    long_text = 'a' * 101
    with pytest.raises(Exception):
        question.add_choice(long_text, False)

def test_generate_choice_id_after_removal():
    # testa se, após remover uma escolha, o ID da nova escolha é gerado com base na última escolha presente
    question = Question(title='Teste de geração de ID após remoção')
    choice1 = question.add_choice('Escolha 1', False)
    choice2 = question.add_choice('Escolha 2', False)
    choice3 = question.add_choice('Escolha 3', False)
    question.remove_choice_by_id(choice2.id)
    choice4 = question.add_choice('Escolha 4', False)
    assert choice4.id == choice3.id + 1

@pytest.fixture
def multiple_choice_question():
    # cria uma questão com três escolhas: duas corretas e uma incorreta.
    q = Question(title="Pergunta com múltiplas escolhas", points=5, max_selections=2)
    q.add_choice("Opção A", False)  # ID 1
    q.add_choice("Opção B", True)   # ID 2
    q.add_choice("Opção C", True)   # ID 3
    return q

def test_fixture_choice_count(multiple_choice_question):
    # testa se a questão criada pela fixture possui exatamente 3 escolhas.
    assert len(multiple_choice_question.choices) == 3

def test_fixture_select_correct_choices(multiple_choice_question):
    # testa se, ao selecionar as escolhas, o método retorna somente os IDs das escolhas corretas.
    selected_ids = multiple_choice_question.select_choices([2, 3])
    assert selected_ids == [2, 3]

def test_fixture_remove_choice_effect(multiple_choice_question):
    # remove a escolha com ID 3, que é correta
    multiple_choice_question.remove_choice_by_id(3)
    selected_ids = multiple_choice_question.select_choices([2, 3])
    assert selected_ids == [2]
