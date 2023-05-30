import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: '/',
    component: () => import('@/pages/Layout/layout.vue'),
    redirect: { name: 'generate' },
    children: [
      {
        path: 'generate',
        name: 'generate',
        component: () => import('@/pages/Generate.vue'),
      },
      {
        path: 'refine',
        name: 'refine',
        component: () => import('@/pages/Refine.vue'),
      },
      {
        path: 'modify',
        name: 'modify',
        component: () => import('@/pages/Modify.vue'),
      },
    ],
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
