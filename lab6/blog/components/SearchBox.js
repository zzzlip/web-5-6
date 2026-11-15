/**
 * 子组件：搜索框
 * 不直接修改父组件数据：用 v-model 绑定到本地 modelValue，
 * 输入时 $emit 自定义事件 update:modelValue / search，由父组件决定如何处理
 */
const SearchBox = {
  props: {
    modelValue: { type: String, default: '' },
    feedback: { type: String, default: '' }
  },
  emits: ['update:modelValue', 'search', 'reset'],
  template: `
    <form class="search-bar" @submit.prevent="$emit('search', modelValue)">
      <input
        type="text"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        placeholder="输入关键字搜索文章标题，如：Vue">
      <button type="submit">搜索</button>
      <button type="button" class="ghost" @click="$emit('reset')">重置</button>
      <p class="feedback">
        {{ feedback }}
        <template v-if="modelValue">（当前关键字：<em>{{ modelValue }}</em>）</template>
      </p>
    </form>
  `
};
