<template>
  <div>
    <v-snackbar
      v-model="this.isAlert"
      multi-line
      elevation="24"
      color="deep-purple-accent-4"
      location="top"
      timeout="2000"
    >
      {{ this.alertMsg }}
      <template v-slot:actions>
        <v-btn color="white" variant="text" @click="this.isAlert = false">
          X
        </v-btn>
      </template>
    </v-snackbar>
    <v-textarea
      class="pt-30"
      label="Enter your prompt here"
      :placeholder="this.ps"
      variant="solo"
      v-model="this.prompt"
      rows="4"
      focused
      maxlength="200"
      counter
    ></v-textarea>
    <div class="d-flex grid-gap-15 mb-15">
      <v-autocomplete
        hide-details
        color="white"
        bg-color="rgba(166, 182, 226, 1)"
        label="조명과 분위기"
        :items="this.lamOpt"
        v-model="this.lam"
        multiple
        chips
        class="w-30"
      ></v-autocomplete>
      <v-autocomplete
        hide-details
        color="white"
        bg-color="rgba(166, 182, 226, 1)"
        label="artistic style and mediums"
        :items="this.asamOpt"
        v-model="this.asam"
        multiple
        chips
        class="w-30"
      ></v-autocomplete>
      <v-autocomplete
        color="white"
        hide-details
        bg-color="rgba(166, 182, 226, 1)"
        label="picture style and quality"
        :items="this.psaqOpt"
        v-model="this.psaq"
        multiple
        chips
        class="w-30"
      ></v-autocomplete>
    </div>
    <v-file-input
      label="Upload Image"
      color="white"
      bg-color="rgba(166, 182, 226, 1)"
      v-model="this.inputImg"
      @update:modelValue="inputChng()"
      accept="image/*"
      show-size
      :rules="this.imgInputRule"
    ></v-file-input>
    <div id="painterro" ref="painterro" class="mb-20"></div>
    <div class="mb-15 text-right">
      <v-btn rounded="xl" size="x-large" class="btn-style-2" @click="runBtn"
        >RUN</v-btn
      >
    </div>
    <div class="font-weight-500 font-20 pb-10">{{ this.modeledPrompt }}</div>
    <v-card height="500px" class="d-flex ai-c justify-content-center">
      <v-img
        default
        class="modeledImg"
        style="height: 32px; width: 32px"
        src="/src/assets/img/default_img.png"
      ></v-img>
      <div
        v-show="this.isModel"
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
<script>
import Painterro from 'painterro';
import axios from 'axios';
import { reactive, nextTick } from 'vue';

export default {
  setup() {
    const baseURL = import.meta.env.VITE_API_ENDPOINT;
    const api = axios.create({
      baseURL,
      timeout: 100000,
    });
    return {
      api,
    };
  },
  data() {
    return {
      imgInputRule: [
        value => {
          if (value[0].size > 2000000) {
            return '이미지는 최대 2MB까지 업로드 가능합니다.';
          }
          return true;
        },
      ],
      isAlert: false,
      alertMsg: null,
      ps: '■ 작성 규칙 : 문장, 단어 상관없이 구분자를 "," 로 작성하기 \n    example 1. 예쁜 고양이가 케이크를 먹는다., 케이크는 초코 케이크, 옆에는 사탕을 먹는 여자아이가 있다., 꿈\n    example 2. 사무실, 여자, 3명, 안경을 낀, 마시다, 커피',
      painterro: null,
      inputImg: [],
      prompt: null,
      lamOpt: [
        '35mm 조명',
        '날카로운 조명',
        '로우폴리 3d 렌더',
        '황금 시간대',
        '맑은 하늘',
        '초현실적인 분위기',
        '에픽 스케일',
        '경이로운 분위기',
        '하이퍼맥시멀리스트',
        '높은 수준의 디테일',
        '아트스테이션 HQ',
        '80mm 조명',
        '포토샵',
        '극도의 디테일',
        '복잡한 분위기',
        '브러쉬 효과',
        '매크로 렌즈',
        '골격 구조 강조',
        '무광 페인팅',
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
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.painterro = Painterro({
        id: 'painterro',
        hiddenTools: ['arrow', 'close', 'bucket', 'open', 'text', 'save'],
        backplateImgUrl: '/src/assets/img/modify_default.png',
        saveHandler: async (image, done) => {
          var blobimg = image.asBlob();
          if (blobimg.size != 10775) {
            var formData = new FormData();
            formData.append('in_files', this.inputImg[0]);

            var file = new File([blobimg], 'mask.png', {
              type: 'image/png',
            });
            formData.append('in_files', file);
            formData.append('prompt', this.prompt);
            formData.append('options1', this.lam);
            formData.append('options2', this.asam);
            formData.append('options3', this.psaq);

            this.isModel = true;

            var result = await this.api.post('/Modify', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            });

            this.isModel = false;
            this.modeledPrompt = result.data['txt'];
            this.modeledImg = result.data['img'];

            var elements2 = document.getElementsByClassName(
              'v-img__img v-img__img--contain',
            );
            elements2[0].src = 'data:image/png;base64,' + result.data['img'];

            this.$nextTick(() => {
              var elements1 = document.getElementsByClassName('modeledImg');
              elements1[0].style.height = '360px';
              elements1[0].style.width = 'unset';
            });
          } else {
            this.isAlert = true;
            this.alertMsg = '이미지에 마스킹 영역을 표시해주세요!';
          }
          done(false);
        },
      });
      this.painterro.show();
    });
  },
  methods: {
    inputChng: function () {
      if (this.inputImg[0].size > 2000000) {
        return;
      }
      var elements = document.getElementsByClassName('ptro-center-tablecell');
      if (this.inputImg[0] == null) {
        elements[0].style.backgroundImage =
          'url(/src/assets/img/modify_default.png)';
      } else {
        elements[0].style.backgroundImage =
          "url('" + window.URL.createObjectURL(this.inputImg[0]) + "')";
      }
    },
    runBtn: function () {
      if (this.prompt == null) {
        this.isAlert = true;
        this.alertMsg = '텍스트를 입력하세요!';
        return;
      }
      // else if (this.lam == null) {
      //   this.isAlert = true;
      //   this.alertMsg = 'lighting and mood를 선택하세요!';
      //   return;
      // } else if (this.asam == null) {
      //   this.isAlert = true;
      //   this.alertMsg = 'artistic style and mediums를 선택하세요!';
      //   return;
      // } else if (this.psaq == null) {
      //   this.isAlert = true;
      //   this.alertMsg = 'picture style and quality를 선택하세요!';
      //   return;
      // }
      if (this.inputImg[0] == null) {
        this.isAlert = true;
        this.alertMsg = '이미지를 업로드하세요!';
        return;
      }
      if (this.inputImg[0].size > 2000000) {
        this.isAlert = true;
        this.alertMsg = '이미지는 최대 2MB까지 업로드 가능합니다.';
        return;
      }
      this.painterro.save();
    },
    fnShareBtn: async function () {
      if (this.modeledImg) {
        var a = document.createElement('a');
        a.href = 'data:image/png;base64,' + this.modeledImg;
        a.download = 'WAI_StableDiffusion_MODIFY.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
    },
    fnResetBtn: async function () {
      this.inputImg = [];
      this.isModel = false;
      this.prompt = '';
      this.lam = null;
      this.asam = null;
      this.psaq = null;
      this.modeledImg = null;
      this.modeledPrompt = null;
      this.modeledImg = null;
      var elements2 = document.getElementsByClassName(
        'v-img__img v-img__img--contain',
      );
      elements2[0].src = '/src/assets/img/default_img.png';
      this.$nextTick(() => {
        var elements1 = document.getElementsByClassName('modeledImg');
        elements1[0].style.height = '32px';
        elements1[0].style.width = '32px';
      });
      var elements = document.getElementsByClassName('ptro-center-tablecell');
      elements[0].style.backgroundImage =
        'url(/src/assets/img/modify_default.png)';
    },
  },
};
</script>
