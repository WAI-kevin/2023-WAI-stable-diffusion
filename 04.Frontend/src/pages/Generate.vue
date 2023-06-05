<template>
  <div>
    <v-textarea
      class="pt-30"
      label="Enter your prompt here"
      variant="solo"
      v-model="data.prompt"
      rows="4"
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
      <v-autocomplete
        hide-details
        color="white"
        bg-color="rgba(166, 182, 226, 1)"
        label="Theme"
        :items="['Theme1', 'Theme2', 'Theme3']"
      ></v-autocomplete>
    </div>
    <div class="mb-15 text-right">
      <v-btn rounded="xl" size="x-large" class="btn-style-2" @click="runBtn"
        >RUN</v-btn
      >
    </div>
    <v-card>
      <v-card-text
        ><v-textarea
          label="Your Prompt"
          variant="underlined"
          readonly
          v-model="resultPrompt"
        ></v-textarea>
      </v-card-text>
      <v-img
        default
        class="mb-30"
        height="400px"
        src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
      ></v-img
    ></v-card>
    <div class="d-flex pt-30 justify-content-space-between">
      <v-btn variant="flat" rounded="xl" class="btn-style-2" @click="fnShareBtn"
        >SHARE</v-btn
      >
      <v-btn variant="flat" rounded="xl" class="btn-style-2">RESET</v-btn>
    </div>
  </div>
</template>
<script setup>
import axios from 'axios';
import { reactive } from 'vue';

const baseURL = import.meta.env.VITE_API_ENDPOINT;
const api = axios.create({
  baseURL,
  timeout: 100000,
});

const fnShareBtn = async () => {
  //
};

const data = reactive({
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
});

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
  }

  var formData = new FormData();
  formData.append('prompt', data.prompt);
  formData.append('options', data.lam);
  formData.append('options', data.asam);
  formData.append('options', data.psaq);

  var result = await api.post('/Generate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  if (result != 'success') {
    console.log(result);
  }
};

const resultPrompt =
  'The Woodman set to work at once, and so sharp was his axe that the tree was soon chopped nearly through.';
</script>
