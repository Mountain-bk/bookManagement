import Vue from 'vue'
import VueRouter from 'vue-router';
import Book from './views/Book.vue'
import BookList from './views/BookList.vue'
import BookRegister from './views/BookRegister.vue'
import Author from './views/Author.vue'
import AuthorList from './views/AuthorList.vue'
import AuthorRegister from './views/AuthorRegister.vue'
import Category from './views/Category.vue'
import CategoryList from './views/CategoryList.vue'
import CategoryRegister from './views/CategoryRegister.vue'
import Home from './views/Home.vue'
// import App from './App.vue'

Vue.use(VueRouter);

export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
        },
        {
            path: '/book-list',
            name: 'book-list',
            component: BookList,
        },
        {
            path: '/book/:id',
            name: 'book',
            component: Book,
        },
        {
            path: '/book-register',
            name: 'book-register',
            component: BookRegister,
        },
        {
            path: '/author-list',
            name: 'author-list',
            component: AuthorList,
        },
        {
            path: '/author/:id',
            name: 'author',
            component: Author,
        },
        {
            path: '/author-register',
            name: 'author-register',
            component: AuthorRegister,
        },
        {
            path: '/category-list',
            name: 'category-list',
            component: CategoryList,
        },
        {
            path: '/category/:id',
            name: 'category',
            component: Category,
        },
        {
            path: '/category-register',
            name: 'category-register',
            component: CategoryRegister,
        },
    ],
});
