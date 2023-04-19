

class BaseService {
    BASE_URL = '/frontend_api';
    async get(url) {
        const response = await fetch(this.BASE_URL + url, {
            method: 'GET'
        });
        return response.json()
    }

    async post(url, body) {
        const response = await fetch(this.BASE_URL + url, {
            headers: {
                'Content-Type': 'application/json',
            },
            method: 'POST',
            body: JSON.stringify(body),
        })
        return await response.json();
    }
}



export class QuestionnaireService extends BaseService {
    async get_questionnaire(questionnaire_id) {
        return await this.get(`/get_questionnaire/${questionnaire_id}/`);
    }
    async create_question(questionnaire_id, text) {
        return await this.post(`/create_question/`, {
            questionnaire_id, text
        });
    }
    async update_question(question_id, text) {
        return await this.post(`/update_question/`, {
            question_id, text
        });

    }
    async delete_question(question_id) {
        return await this.post(`/delete_question/`, {
            question_id
        });

    }
    async create_answer(question_id, text) {
        return await this.post(`/create_answer/`, {
            question_id, text
        });

    }
    async update_answer(answer_id, text) {
        return await this.post(`/update_answer/`, {
            answer_id, text
        });

    }
    async delete_answer(answer_id) {
        return await this.post(`/delete_answer/`, {
            answer_id
        });

    }
    async create_relation(to_question_id, from_question_id, from_answer_id) {

        return await this.post(`/create_relation/`, {
            to_question_id, from_question_id, from_answer_id
        });
    }
    async update_relation(relation_id, update_data) {
        return await this.post(`/update_relation/`, {
            relation_id, update_data
        });
    }
    async delete_relation(relation_id) {
        return await this.post(`/delete_relation/`, {
            relation_id
        });
    }
}
