<template>
    <div class="question">
        <div class="question__id">{{ question.id }}</div>
        <div class="question__text">
            {{ question.text }}
        </div>
        <div class="question__answers">
            <div class="question__answer"
                 :class="{
                     '--selected': selectedAnswer && selectedAnswer.id === answer.id,
                 }"
                :ref="'questionAnswer__' + answer.id"
                v-for="answer in question.answers">
                <div class="question__answer-id">{{ answer.id }}</div>
                <div class="question__answer-text">{{ answer.text }}</div>
            </div>
            <div class="question__answer">
                <button @click="$emit('edit-question')">Edit</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "question",
    props: ['question', 'selectedAnswer']
}
</script>

<style>

</style>