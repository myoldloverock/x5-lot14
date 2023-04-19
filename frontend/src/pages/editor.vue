<template>
    <div>
        <div class="toolbar">
            <button @click="openAddQuestion">Add question</button>
            <button v-show="direction === 'horizontal'"
                    @click="setDirection('vertical')">
                Vertical view
            </button>
            <button v-show="direction === 'vertical'"
                    @click="setDirection('horizontal')">
                Horizontal view
            </button>
            <button @click="openAddRelation">Add relation</button>
            <button @click="deleteRelation" :disabled="!selectedRelation">
                Delete relation
            </button>
        </div>
        <div class="dialog" v-show="showQuestionDialog">
            <fieldset style="max-width: 320px;">
                <h4 v-if="!editQuestionId">Add question</h4>
                <h4 v-else>
                    Change Question #{{ editQuestionId }}
                    <button @click="deleteQuestion">Delete</button>
                </h4>
                <div>
                    <label for="addQuestion__text">Question text:</label><br>
                    <textarea id="addQuestion__text" v-model="questionForm__text" />
                </div>
                <div style="padding-left: 16px">
                    <div v-for="(addQuestion__answer, i) in questionForm__answers"
                         style="border-left: 3px solid gray; padding-left: 16px; margin-bottom: 16px">
                        <h5 style="margin: 8px 0">Answer {{ i + 1 }}</h5>
                        <label for="addQuestion__answer0-text">Answer text:</label><br>
                        <textarea id="addQuestion__answer0-text" v-model="addQuestion__answer.text" />
                        <button @click="deleteAnswer(addQuestion__answer)">Remove</button>
                    </div>
                    <button @click="questionForm__answers.push({text: ''})">Add answer</button>
                </div>
                <div v-if="!editQuestionId">
                    <label>Parent:</label><br>
                    <select v-model="questionForm__parentQuestion">
                        <option :value="null">-</option>
                        <option :value="question.id"
                                v-for="question in questions">
                            [{{ question.id }}]
                            {{ question.text }}
                        </option>
                    </select>
                    <select v-if="questionForm__parentQuestion !== null"
                            v-model="questionForm__parentAnswer">
                        <option :value="null">-</option>
                        <option :value="answer.id"
                                v-for="answer in findQuestionById(questionForm__parentQuestion).answers">
                            [{{ answer.id }}]
                            {{ answer.text }}
                        </option>
                    </select>
                </div>
                <button v-if="editQuestionId" @click="saveQuestion">Save question</button>
                <button v-else @click="addQuestion">Add question</button>
                <button @click="showQuestionDialog = false">Close</button>
            </fieldset>
        </div>
        <div class="dialog" v-show="showRelationDialog">
            <fieldset style="max-width: 320px;">
                <h4 v-if="!editRelationId">Add relation</h4>
                <h4 v-else>Change relation</h4>
                <div>
                    From: <br>
                    <select v-model="relationForm__fromQuestionId">
                        <option :value="null">No</option>
                        <option :value="question.id" v-for="question in questions">
                            [{{ question.id }}] {{ question.text }}
                        </option>
                    </select>
                    <select v-if="relationForm__fromQuestionId"
                            v-model="relationForm__fromAnswerId">
                        <option :value="null">No</option>
                        <option :value="answer.id" v-for="answer in findQuestionById(relationForm__fromQuestionId).answers">
                            [{{ answer.id }}] {{ answer.text }}
                        </option>
                    </select>
                </div>
                <div>
                    To: <br>
                    <select v-model="relationForm__toQuestionId">
                        <option :value="null">No</option>
                        <option :value="question.id" v-for="question in questions">
                            [{{ question.id }}] {{ question.text }}
                        </option>
                    </select>
                </div>
                <button v-if="!editRelationId" @click="addRelation">Create</button>
                <button v-else>Update</button>
            </fieldset>
        </div>

        <div class="relations"
             :class="{
                 '--vertical': direction === 'vertical',
                 '--horizontal': direction === 'horizontal',
             }">
            <div class="relations__stages">
                <svg class="lines-svg">
                    <g class="relation-line"
                       :class="{
                           '--active': selectedRelation && line.relation === selectedRelation,
                       }"
                       v-for="line in lines">
                        <line
                            @click="selectRelation(line.relation)"
                            :x1="line.x1"
                            :x2="line.x2"
                            :y1="line.y1"
                            :y2="line.y2" />
                    </g>
                </svg>
                <div class="relations__stage" v-for="stage in stages">
                    <question
                        v-for="(question, questionIndex) in stage"
                        :ref="'stageQuestion__' + question.id"
                        :key="'stageQuestion' + questionIndex"
                        :question="question"
                        :selected-answer="selectedAnswer"
                        @edit-question="openQuestionEditor(question.id)"
                    />
                </div>

                <div class="connectors" style="position:absolute;top:0;left:0;">
                    <div class="connector --from"
                         :class="{
                             '--active': selectedRelation && selectedRelation.from_question_id === connector.question.id,
                         }"
                         v-for="connector in connectors"
                         :style="selectorStyles(connector, 'from')">
                    </div>
                    <div class="connector --to"
                         :class="{
                             '--active': selectedRelation && selectedRelation.to_question_id === connector.question.id,
                         }"
                         v-for="connector in connectors"
                         :style="selectorStyles(connector, 'to')">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Question from "@/components/question.vue";
import {QuestionnaireService} from "@/service";

Array.prototype.insert = function(index, ...items) {
    this.splice(index, 0, ...items);
};

const $service = new QuestionnaireService();

export default {
    name: 'App',
    data: () => ({
        questions: [],
        connectors: [],
        connectorsLines: [],
        stages: [[]],
        direction: 'vertical',
        relations: [],
        lines: [],

        selectedRelation: null,
        selectedAnswer: null,

        questionForm__text: '',
        questionForm__answers: [
            { text: '' }
        ],
        questionForm__parentQuestion: null,
        questionForm__parentAnswer: null,

        relationForm__fromQuestionId: null,
        relationForm__fromAnswerId: null,
        relationForm__toQuestionId: null,

        showQuestionDialog: false,
        showRelationDialog: false,
        editQuestionId: null,
        editRelationId: null,
    }),
    methods: {
        openAddQuestion() {
            this.editQuestionId = null;
            this.showQuestionDialog = true;

            this.questionForm__text = '';
            this.questionForm__answers = [
                { text: '' }
            ];
            this.questionForm__parentQuestion = null;
            this.questionForm__parentAnswer = null;
        },

        openAddRelation() {
            this.editRelationId = null;
            this.showRelationDialog = true;

            this.relationForm__fromQuestionId = null;
            this.relationForm__fromAnswerId = null;
            this.relationForm__toQuestionId = null;
        },

        openQuestionEditor(questionId) {
            this.editQuestionId = questionId;
            this.showQuestionDialog = true;
            const question = this.findQuestionById(questionId);
            this.questionForm__text = question.text;
            this.questionForm__answers = question.answers;

            const relations_TO = this.findQuestionRelations_TO(questionId);
            if (relations_TO.length) {
                this.questionForm__parentQuestion = relations_TO[0].from_question_id;
                this.questionForm__parentAnswer = relations_TO[0].from_answer_id;
            }
        },
        async addQuestion() {
            const questionId = await $service.create_question(this.questionnaireId, this.questionForm__text);
            const question = {
                id: questionId,
                text: this.questionForm__text,
                stage: null,
            }
            const answers = [];
            for (const answer of this.questionForm__answers) {
                const answerId = await $service.create_answer(questionId, answer.text);
                answers.push({
                    id: answerId,
                    text: answer.text,
                })
            }
            question.answers = answers;
            this.questions.push(question);

            if (this.questionForm__parentQuestion) {
                const relationId = await $service.create_relation(
                    questionId,
                    this.questionForm__parentQuestion,
                    this.questionForm__parentAnswer
                )
                this.relations.push({
                    id: relationId,
                    from_question_id: this.questionForm__parentQuestion,
                    from_answer_id: this.questionForm__parentAnswer,
                    to_question_id: question.id,
                })
            }

            this.updateStages();

            this.questionForm__text = '';
            this.questionForm__answers = [{text: ''}];
            this.questionForm__parentAnswer = null;
            this.questionForm__parentQuestion = null;
        },
        async saveQuestion() {
            for (const answer of this.questionForm__answers) {
                if (!answer.id) {
                    answer.id = await $service.create_answer(this.editQuestionId, answer.text);
                } else {
                    await $service.update_answer(answer.id, answer.text);
                }
            }

            await $service.update_question(this.editQuestionId, this.questionForm__text);

            this.showQuestionDialog = false;

            this.updateStages();
        },
        async deleteQuestion() {
            await $service.delete_question(this.editQuestionId);
            const questions = [];
            for (const question of this.questions) {
                if (question.id !== this.editQuestionId) {
                    questions.push(question)
                }
            }
            this.questions = questions;

            const relations = [];
            for (const relation of this.relations) {
                if (relation.from_question_id === this.editQuestionId ||
                    relation.to_question_id === this.editQuestionId) {
                } else {
                    relations.push(relation);
                }
            }
            this.relations = relations;

            this.editQuestionId = null;
            this.showQuestionDialog = false;

            this.updateStages();
        },
        async addRelation() {
            const relationId = await $service.create_relation(
                this.relationForm__toQuestionId,
                this.relationForm__fromQuestionId,
                this.relationForm__fromAnswerId,
            )
            this.relations.push({
                id: relationId,
                to_question_id: this.relationForm__toQuestionId,
                from_question_id: this.relationForm__fromQuestionId,
                from_answer_id: this.relationForm__fromAnswerId,
            });

            this.showRelationDialog = false;

            this.updateStages()
        },
        async deleteAnswer(answer) {
            if (answer.id) {
                await $service.delete_answer(answer.id)
            }
            this.questionForm__answers.splice(this.questionForm__answers.indexOf(answer), 1);
        },

        selectorStyles(connector, /** @type {'from' | 'to'} */ direction) {
            const values = direction === 'from'
                ? this.fromSelectorValues(connector)
                : this.toSelectorValues(connector);
            return {
                'position': 'absolute',
                'left': `${values.left}px`,
                'top': `${values.top}px`,
            }
        },
        fromSelectorValues(connector) {
            if (this.direction === 'vertical') {
                return {
                    'left': connector.offsetLeft + connector.rect.width / 2,
                    'top': connector.offsetTop + connector.rect.height,
                };
            }
            return {
                'left': connector.offsetLeft + connector.rect.width,
                'top': connector.offsetTop + connector.rect.height / 2,
            };
        },
        toSelectorValues(connector) {
            if (this.direction === 'vertical') {
                return {
                    'left': connector.offsetLeft + connector.rect.width / 2,
                    'top': connector.offsetTop,
                };
            }
            return {
                'left': connector.offsetLeft,
                'top': connector.offsetTop + connector.rect.height / 2,
            };
        },
        updateStages() {
            for (const question of this.questions) {
                question.stageFound = false;
            }
            this.stages = this.parseRelationsAsStages();
            this.moveAllOneStageRelationsToBottom();
            this.moveNoFromQuestionsToBegin();
            this.updateConnectors();
        },
        parseRelationsAsStages() {
            const lastQuestionsIds = [];
            for (const question of this.questions) {
                const relations = this.findQuestionRelations_FROM(question.id);
                if (relations.length) continue;
                lastQuestionsIds.push(question);
                question.stageFound = true;
            }
            const stages = [];
            let stage = lastQuestionsIds;
            stages.unshift(stage);
            while (stage.length) {
                stage = this.findStageQuestions(stage);
                if (stage.length) stages.unshift(stage);
            }
            return stages;
        },

        findStageQuestions(/** @type {Array<number>} */ stage) {
            const newStage = [];
            for (const question of stage) {
                const relations = this.findQuestionRelations_TO(question.id);
                const fromQuestions = relations.map(rel => rel.from_question_id);
                for (const fromQuestionId of fromQuestions) {
                    const fromQuestion = this.findQuestionById(fromQuestionId);
                    if (!fromQuestion.stageFound) {
                        newStage.push(fromQuestion);
                        fromQuestion.stageFound = true;
                    }
                }
            }
            return newStage;
        },

        findQuestionStageIndex(questionId) {
            for (let i = 0; i < this.stages.length; ++i) {
                const stage = this.stages[i];
                for (const question of stage) {
                    if (question.id === questionId) return i;
                }
            }
            return -1;
        },

        moveAllOneStageRelationsToBottom() {
            let relation = this.oneStageRelation();
            while (relation) {
                this.moveQuestionToNextStage(relation.to_question_id);
                relation = this.oneStageRelation();
            }
        },

        moveNoFromQuestionsToBegin() {
            for (const question of this.questions) {
                const relations_TO = this.findQuestionRelations_TO(question.id);
                if (relations_TO.length) continue;
                this.moveQuestionToBegin(question.id);
            }
        },

        oneStageRelation() {
            for (const relation of this.relations) {
                const from = this.findQuestionStageIndex(relation.from_question_id);
                const to = this.findQuestionStageIndex(relation.to_question_id);
                if (from === to) {
                    return relation;
                }
            }
            return null;
        },

        moveQuestionToNextStage(questionId) {
            const oldStageIndex = this.findQuestionStageIndex(questionId);
            const newStageIndex = oldStageIndex + 1;
            this.moveQuestion(questionId, oldStageIndex, newStageIndex);
            for (const relation of this.findQuestionRelations_FROM(questionId)) {
                this.moveQuestionToNextStage(relation.to_question_id);
            }
            this.updateConnectors()
        },

        moveQuestionToBegin(questionId) {
            const oldStageIndex = this.findQuestionStageIndex(questionId);
            this.moveQuestion(questionId, oldStageIndex, 0);
            this.updateConnectors()
        },

        moveQuestion(questionId, oldStageIndex, newStageIndex) {
            const stages = [...this.stages];
            while (stages.length <= newStageIndex) {
                stages.push([]);
            }
            const oldStage = stages[oldStageIndex];
            const oldQuestionIndex = oldStage.findIndex(el => el.id === questionId);
            const question = oldStage[oldQuestionIndex];
            oldStage.splice(oldQuestionIndex, 1);
            const newStage = stages[newStageIndex];
            newStage.insert(oldQuestionIndex, question);
            this.stages = stages;

        },

        findQuestionRelations_TO(questionId) {
            const result = [];
            for (const relation of this.relations) {
                if (relation.to_question_id === questionId) {
                    result.push(relation);
                }
            }
            return result;
        },
        findQuestionRelations_FROM(questionId) {
            const result = [];
            for (const relation of this.relations) {
                if (relation.from_question_id === questionId) {
                    result.push(relation);
                }
            }
            return result;
        },
        findQuestionById(questionId) {
            return this.questions.find(el => el.id === questionId);
        },
        async updateConnectors() {
            await this.$nextTick();
            const result = [];
            for (const question of this.questions) {
                const refStr = 'stageQuestion__' + question.id;
                if (!(refStr in this.$refs)) continue;
                const ref = this.$refs[refStr][0];
                result.push({
                    question: question,
                    answer: null,
                    rect: ref.$el.getBoundingClientRect(),
                    offsetTop: ref.$el.offsetTop,
                    offsetLeft: ref.$el.offsetLeft,
                    offsetRight: ref.$el.offsetRight,
                })
            }
            this.connectors = result;
            this.drawRelations();
        },
        findConnectorByQuestionId(questionId) {
            for (const connector of this.connectors) {
                if (connector.question.id === questionId) {
                    return connector;
                }
            }
            return null;
        },
        setDirection(value) {
            this.direction = value;
            this.updateStages();
        },
        drawRelations() {
            const result = [];
            for (const relation of this.relations) {
                const line = this.drawRelation(relation.from_question_id, relation.to_question_id);
                if (line) result.push(line);
            }
            this.lines = result;
        },
        drawRelation(fromQuestionId, toQuestionId) {
            const fromConnector = this.findConnectorByQuestionId(fromQuestionId);
            if (!fromConnector) return null;
            const fromSelector = this.fromSelectorValues(fromConnector);

            const toConnector = this.findConnectorByQuestionId(toQuestionId);
            if (!toConnector) return null;
            const toSelector = this.toSelectorValues(toConnector);

            return {
                x1: fromSelector.left,
                y1: fromSelector.top,

                x2: toSelector.left,
                y2: toSelector.top,

                relation: this.findRelation(fromQuestionId, toQuestionId),
            }

        },

        findRelation(fromQuestionId, toQuestionId) {
            for (const relation of this.relations) {
                if (relation.from_question_id === fromQuestionId &&
                    relation.to_question_id === toQuestionId) {
                    return relation;
                }
            }
            return null;
        },
        selectRelation(relation) {
            this.selectedRelation = relation;
            this.selectedAnswer = this.findAnswerById(relation.from_answer_id);

            this.relationForm__fromQuestionId = relation.from_question_id;
            this.relationForm__fromAnswerId = relation.from_answer_id;
            this.relationForm__toQuestionId = relation.to_question_id;

            this.editRelationId = relation.id;
            this.showRelationDialog = true;
        },
        findAnswerById(answerId) {
            for (const question of this.questions) {
                for (const answer of question.answers) {
                    if (answer.id === answerId) return answer;
                }
            }
            return null;
        },
        async deleteRelation() {
            const relationIndex = this.relations.indexOf(this.selectedRelation);
            await $service.delete_relation(this.selectedRelation.id);
            this.relations.splice(relationIndex, 1);
            this.selectedRelation = null;
            this.selectedAnswer = null;
            this.updateStages();
        },
    },
    computed: {
        questionnaireId() {
            return this.$route.params.questionnaireId;
        }
    },
    async created() {
        const { questions, relations } = await $service.get_questionnaire(this.questionnaireId);
        this.questions = questions;
        this.relations = relations;
        this.updateStages();
    },
    components: {
        Question,
    }
}
</script>

<style lang="stylus">
$relation-common = #207ae1
$relation-hover = #E15720
$relation-active = #2de120

.free-questions
    display flex
    flex-wrap wrap

.relation-line
    stroke $relation-common
    stroke-width 4px
    cursor pointer
    transition .2s

    &:hover
        stroke $relation-hover

    &.--active
        stroke $relation-active

.question
    padding 8px
    margin 16px
    border 1px solid orange
    max-width 256px
    position relative
    text-align center

    &__id
        position absolute
        padding 0
        font-size 10px
        color gray
        right 0
        top 0

    &__text
        font-weight bold
        font-size 13px
        cursor grab

    &__answers
        border-top 1px solid gray
        margin-top 4px
        padding-top 4px

    &__answer
        position relative
        margin 8px 0
        padding 4px

        &.--selected
            background #9bff9b

    &__answer-id
        background brown
        position absolute
        padding 0 2px
        font-size 9px
        border-radius 8px
        color white
        right -6px
        top -6px

    &__answer-text
        font-size 12px
        text-align left


.relations
    padding-bottom 256px

    &__stage
        min-width 192px
        margin 0
        display flex
        justify-content center
        align-items center

    &__stages
        display flex
        flex-wrap nowrap
        overflow-x auto
        position relative

.relations.--horizontal .relations__stage
    flex-direction column

.relations.--horizontal .relations__stages
    flex-direction row

.relations.--vertical .relations__stage
    flex-direction row

.relations.--vertical .relations__stages
    flex-direction column


.connector
    width 8px
    height 8px
    border-radius 50%
    margin-left -4px
    margin-top -4px
    background $relation-common
    transition width .2s, height .2s, margin .2s
    cursor pointer

    &:hover
        width 16px
        height 16px
        margin-left -8px
        margin-top -8px
        background $relation-hover

    &.--active
        background $relation-active


.lines-svg
    width 100%
    height 100%
    position absolute
    left 0
    top 0

</style>
