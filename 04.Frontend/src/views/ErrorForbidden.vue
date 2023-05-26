<template>
  <section class="error errorforbidden">
    <div class="container">
      <div class="txt-group">
        <div class="txt">403 FORBIDDEN</div>
        <div class="txt2">
          죄송합니다. 사용자 인증이 필요합니다. <br />그룹웨어를 통해 들어
          오시기 바랍니다.
        </div>
        <router-link to="https://ep.joins.net" class="btn">홈으로</router-link>
      </div>

      <img src="@/assets/img/img_error1.svg" alt=" " class="img-error" />
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  error: Object,
});
</script>

<style scoped></style>
