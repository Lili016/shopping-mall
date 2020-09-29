var vm = new Vue({
    el: "#updatepass",
    data: {
        host: host,
        token: sessionStorage.token || localStorage.token,
        oldpassword: '',
        newpassword1: '',
        newpassword2: ''
    },
    methods: {
        on_submit: function(){
            axios.put(
                this.host + '/users/',
                {
                    oldpassword: this.oldpassword,
                    newpassword1: this.newpassword1,
                    newpassword2: this.newpassword2
                },
                {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json'
                }
            )
            .then(response => {
            })
            .catch(error => {
            });
        }
    }
});