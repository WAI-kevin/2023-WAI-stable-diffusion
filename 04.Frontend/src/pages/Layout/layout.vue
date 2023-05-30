<template>
  <div class="layout">
    <div class="main-panel">
      <top-nav></top-nav>
      <suspense>
        <router-view class="main-content"></router-view>
      </suspense>
      <footer-bar></footer-bar>
    </div>
  </div>
</template>
<script setup>
import SideNav from '@/components/SideNav.vue';
import TopNav from '@/components/TopNav.vue';
import FooterBar from '@/components/FooterBar.vue';
</script>
