import VueRouter from "vue-router";
import Editor from "@/pages/editor.vue";


const routes = [
    {
        path: '/editor/:questionnaireId/',
        component: Editor,
    }
]

export const router = new VueRouter({
    routes,
    mode: 'history',
});
