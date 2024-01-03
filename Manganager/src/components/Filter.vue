<template>
    <div>
        <div>
            <q-checkbox 
                v-model="finished" 
                @update:model-value="send_event()"
                label="Not finished"
            />
        </div>
        <div>
            Sort by:
            
            <q-checkbox v-model="date" @update:model-value="this.sorting('date')"/>
            <label>Date</label>
            
            <q-checkbox v-model="remaining" @update:model-value="this.sorting('remaining')"/>
            <label>Remaining chapters</label>
            
            <q-checkbox v-model="site" @update:model-value="this.sorting('site')"/>
            <label>Sites</label>
        </div>
    </div>
</template>

<script>


export default{
    name: "Filter",
    data(){
        return {
            finished:false,
            sort: "date",
            date: false,
            remaining: false,
            site: false,
        }
    },
    methods:{
        sorting(type) {
            switch(type) {
                case 'date':
                    this.remaining = false
                    this.site = false
                case 'remaining':
                    this.date = false
                    this.site = false
                case 'site':
                    this.date = false
                    this.remaining = false
            }
            this.sort = type
            this.send_event()
        },
        send_event(){
            this.$emit("filter",this.finished, this.sort)
        }
    }


}
</script>