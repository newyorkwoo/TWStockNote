<template>
  <div class="bg-white rounded-lg shadow p-6 mb-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">日期範圍</h2>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Start Date -->
      <div>
        <label for="start-date" class="block text-sm font-medium text-gray-700 mb-2">
          開始日期
        </label>
        <input
          id="start-date"
          type="date"
          :value="startDate"
          @input="$emit('update:startDate', $event.target.value)"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nasdaq-blue focus:border-transparent"
        />
      </div>

      <!-- End Date -->
      <div>
        <label for="end-date" class="block text-sm font-medium text-gray-700 mb-2">
          結束日期
        </label>
        <input
          id="end-date"
          type="date"
          :value="endDate"
          @input="$emit('update:endDate', $event.target.value)"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-nasdaq-blue focus:border-transparent"
        />
      </div>

      <!-- Apply Button -->
      <div class="flex items-end">
        <button
          @click="$emit('apply')"
          class="w-full px-4 py-2 bg-nasdaq-blue text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          套用
        </button>
      </div>
    </div>

    <!-- Quick Select Buttons -->
    <div class="mt-4 flex flex-wrap gap-2">
      <button
        v-for="preset in presets"
        :key="preset.label"
        @click="applyPreset(preset)"
        class="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors"
      >
        {{ preset.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  startDate: {
    type: String,
    required: true
  },
  endDate: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:startDate', 'update:endDate', 'apply'])

/**
 * Preset date ranges
 */
const presets = [
  {
    label: '最近 1 年',
    getRange: () => ({
      start: new Date(new Date().setFullYear(new Date().getFullYear() - 1))
        .toISOString()
        .split('T')[0],
      end: new Date().toISOString().split('T')[0]
    })
  },
  {
    label: '最近 3 年',
    getRange: () => ({
      start: new Date(new Date().setFullYear(new Date().getFullYear() - 3))
        .toISOString()
        .split('T')[0],
      end: new Date().toISOString().split('T')[0]
    })
  },
  {
    label: '最近 5 年',
    getRange: () => ({
      start: new Date(new Date().setFullYear(new Date().getFullYear() - 5))
        .toISOString()
        .split('T')[0],
      end: new Date().toISOString().split('T')[0]
    })
  },
  {
    label: '最近 10 年',
    getRange: () => ({
      start: new Date(new Date().setFullYear(new Date().getFullYear() - 10))
        .toISOString()
        .split('T')[0],
      end: new Date().toISOString().split('T')[0]
    })
  },
  {
    label: '全部 (2000-至今)',
    getRange: () => ({
      start: '2000-01-01',
      end: new Date().toISOString().split('T')[0]
    })
  }
]

/**
 * Apply preset date range
 */
const applyPreset = (preset) => {
  const range = preset.getRange()
  emit('update:startDate', range.start)
  emit('update:endDate', range.end)
  emit('apply')
}
</script>
