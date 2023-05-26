<template>
  <v-app>
    <router-view></router-view>
  </v-app>
</template>

<script setup>
import { onBeforeMount, onMounted, onBeforeUnmount, reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

onBeforeMount(async () => {});

onMounted(async () => {});
</script>
