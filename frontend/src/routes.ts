import Main from "./Main.vue";

export default [
  {
    path: "/:date?",
    component: Main,
    props: (route) => ({ date: route.params.date || undefined }),
  },
];
