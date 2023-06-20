<template>
  <div>
    <v-textarea
      class="pt-30"
      label="Enter your prompt here"
      :placeholder="data.ps"
      variant="solo"
      v-model="data.prompt"
      rows="4"
      focused
    ></v-textarea>
    <div class="d-flex grid-gap-15 mb-15">
      <v-autocomplete
        hide-details
        color="white"
        bg-color="rgba(166, 182, 226, 1)"
        label="lighting and mood"
        :items="data.lamOpt"
        v-model="data.lam"
      ></v-autocomplete>
      <v-autocomplete
        hide-details
        color="white"
        bg-color="rgba(166, 182, 226, 1)"
        label="artistic style and mediums"
        :items="data.asamOpt"
        v-model="data.asam"
      ></v-autocomplete>
      <v-autocomplete
        color="white"
        hide-details
        bg-color="rgba(166, 182, 226, 1)"
        label="picture style and quality"
        :items="data.psaqOpt"
        v-model="data.psaq"
      ></v-autocomplete>
    </div>
    <v-file-input
      label="Upload Image"
      color="white"
      bg-color="rgba(166, 182, 226, 1)"
      v-model="data.inputImg"
    ></v-file-input>
    <div class="mb-15 text-right">
      <v-btn rounded="xl" size="x-large" class="btn-style-2" @click="runBtn"
        >RUN</v-btn
      >
    </div>
    <div class="font-weight-500 font-20 pb-10">{{ data.modeledPrompt }}</div>
    <v-card height="500px" class="d-flex ai-c justify-content-center">
      <v-img
        default
        class="modeledImg"
        style="height: 32px; width: 32px"
        src="/src/assets/img/default_img.png"
      ></v-img>
      <div
        v-show="data.isModel"
        style="width: 150px; background: white; position: absolute"
      >
        <div class="font-weight-500 font-13 pb-10">Modeling Your Image...</div>
        <v-progress-linear
          color="deep-purple-accent-4"
          indeterminate
          rounded
          height="6"
        ></v-progress-linear>
      </div>
    </v-card>
    <div class="d-flex pt-30 justify-content-space-between">
      <v-btn variant="flat" rounded="xl" class="btn-style-2" @click="fnShareBtn"
        >SHARE</v-btn
      >
      <v-btn variant="flat" rounded="xl" class="btn-style-2" @click="fnResetBtn"
        >RESET</v-btn
      >
    </div>
  </div>
</template>
<script setup>
import axios from 'axios';
import { reactive, nextTick } from 'vue';

const baseURL = import.meta.env.VITE_API_ENDPOINT;
const api = axios.create({
  baseURL,
  timeout: 100000,
});

const data = reactive({
  inputImg: [],
  ps: '■ 작성 규칙 : 문장, 단어 상관없이 구분자를 "," 로 작성하기 \n    example 1. 예쁜 고양이가 케이크를 먹는다., 케이크는 초코 케이크, 옆에는 사탕을 먹는 여자아이가 있다., 꿈\n    example 2. 사무실, 여자, 3명, 안경을 낀, 마시다, 커피',
  prompt: '',
  lamOpt: [
    '35mm',
    'sharp',
    'low poly 3d render',
    'golden hour',
    'sunny sky',
    'hyper realistic',
    'epic scale',
    'sense of awe',
    'hypermaximalist',
    'insane level of details',
    'artstation HQ',
    '80mm',
    'photoshopped',
    'insanely detailed',
    'intricate',
    'brush effect',
    'macro',
    'precise correct anatomy',
    'matte painting',
  ],
  lam: null,
  asamOpt: [
    'Pablo Picasso',
    'Van Gogh',
    'Da Vinci',
    'Hokusai',
    'Manga',
    'fantasy',
    'minimalism',
    'abstract',
    'graffiti',
    'Digital art',
    'digital painting',
    'color page',
    'featured on pixiv (for anime/manga)',
    'trending on artstation',
    'precise line-art',
    'tarot card',
    'character design',
    'concept art',
    'symmetry',
    'golden ratio',
    'evocative',
    'award winning',
    'shiny',
    'smooth',
    'surreal',
    'divine',
    'celestial',
    'elegant',
    'oil painting',
    'soft',
    'fascinating',
    'fine art',
    'Oil on canvas',
    'watercolour',
    'sketch',
    'photography',
    'Isometric',
    'pixar',
    'scientific',
    'comic',
  ],
  asam: null,
  psaqOpt: [
    'ultra wide-angle',
    'wide-angle',
    'aerial view',
    'massive scale',
    'street level view',
    'landscape',
    'panoramic',
    'bokeh',
    'fisheye',
    'dutch angle',
    'low angle',
    'extreme long-shot',
    'long shot',
    'close-up',
    'extreme close-up',
    'highly detailed',
    '4k',
    '8k uhd',
    'studio quality',
    'polaroid',
    '100mm',
    'film photography',
    'dslr',
    'cinema4d',
    'movie concept arthighly detailed',
    'grainy',
    'unreal engine',
    'octane render',
    'vray',
    'houdini render',
    'quixel megascans',
    'depth of field (or dof)',
    'arnold render',
    'raytracing',
    'cgi',
    'lumen reflections',
    'cgsociety',
    'realistic',
    'ultra realistic',
    'volumetric fog',
    'overglaze',
    'analog photo',
  ],
  psaq: null,
  modeledImg: null,
  modeledPrompt: null,
  isModel: false,
});

const fnShareBtn = async () => {
  if (data.modeledImg) {
    var a = document.createElement('a');
    a.href = 'data:image/png;base64,' + data.modeledImg;
    a.download = 'WAI_StableDiffusion_REFINE.png';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
};

const fnResetBtn = async () => {
  data.isModel = false;
  data.prompt = '';
  data.lam = null;
  data.asam = null;
  data.psaq = null;
  data.modeledImg = null;
  data.modeledPrompt = null;
  data.modeledImg = null;
  var elements2 = document.getElementsByClassName(
    'v-img__img v-img__img--contain',
  );
  elements2[0].src = '/src/assets/img/default_img.png';
  await nextTick(() => {
    var elements1 = document.getElementsByClassName('modeledImg');
    elements1[0].style.height = '32px';
    elements1[0].style.width = '32px';
  });
};

const runBtn = async () => {
  if (data.prompt == null) {
    console.log('프롬프트를 입력하세요');
    return;
  } else if (data.lam == null) {
    console.log('lighting and mood를 입력하세요');
    return;
  } else if (data.asam == null) {
    console.log('artistic style and mediums를 입력하세요');
    return;
  } else if (data.psaq == null) {
    console.log('picture style and quality를 입력하세요');
    return;
  } else if (data.inputImg[0] == null) {
    console.log('이미지를 입력하세요');
    return;
  }

  var formData = new FormData();
  formData.append('in_files', data.inputImg[0]);
  formData.append('prompt', data.prompt);
  formData.append('options1', data.lam);
  formData.append('options2', data.asam);
  formData.append('options3', data.psaq);

  data.isModel = true;

  var result = await api.post('/Refine', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  data.isModel = false;
  data.modeledPrompt = result.data['txt'];
  data.modeledImg = result.data['img'];

  // var elements2 = document.getElementsByClassName(
  //   'v-img__img v-img__img--contain',
  // );
  // elements2[0].src = 'data:image/png;base64,' + result.data['img'];

  // await nextTick(() => {
  //   var elements1 = document.getElementsByClassName('modeledImg');
  //   elements1[0].style.height = '360px';
  //   elements1[0].style.width = 'unset';
  // });
};
</script>
