def calculate_groundedness(
    answer,
    context
):

    answer_words = set(
        answer.lower().split()
    )

    context_words = set(
        context.lower().split()
    )

    if len(answer_words) == 0:

        return 0.0

    overlap = len(
        answer_words.intersection(
            context_words
        )
    )

    score = overlap / len(
        answer_words
    )

    return round(
        score,
        2
    )


def calculate_relevance(
    question,
    answer
):

    question_words = set(
        question.lower().split()
    )

    answer_words = set(
        answer.lower().split()
    )

    if len(question_words) == 0:

        return 0.0

    overlap = len(
        question_words.intersection(
            answer_words
        )
    )

    score = overlap / len(
        question_words
    )

    return round(
        score,
        2
    )


def evaluate_answer(
    question,
    answer,
    context
):

    return {
        "groundedness": calculate_groundedness(
            answer,
            context
        ),
        "relevance": calculate_relevance(
            question,
            answer
        )
    }