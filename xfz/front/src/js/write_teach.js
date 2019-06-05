function Teach() {
    this.progressGroup = $("#progress-group");
}

Teach.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor',{
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
};

// Teach.prototype.listenUploadFielEvent = function () {
//     var uploadBtn = $('#thumbnail-btn');
//     uploadBtn.change(function () {
//         var file = uploadBtn[0].files[0];
//         var formData = new FormData();
//         formData.append('file',file);
//         xfzajax.post({
//             'url': '/cms/upload_file/',
//             'data': formData,
//             'processData': false,
//             'contentType': false,
//             'success': function (result) {
//                 if(result['code'] === 200){
//                     var url = result['data']['url'];
//                     var thumbnailInput = $("#thumbnail-form");
//                     thumbnailInput.val(url);
//                 }
//             }
//         });
//     });
// };

Teach.prototype.listenQiniuUploadFileEvent = function () {
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if(result['code'] === 200){
                    var token = result['data']['token'];
                    // a.b.jpg = ['a','b','jpg']
                    // 198888888 + . + jpg = 1988888.jpg
                    var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                    var putExtra = {
                        fname: key,
                        params:{},
                        mimeType: ['image/png','image/jpeg','image/gif','video/x-ms-wmv','video/mp4']
                    };
                    var config = {
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z0
                    };
                    var observable = qiniu.upload(file,key,token,putExtra,config);
                    observable.subscribe({
                        'next': self.handleFileUploadProgress,
                        'error': self.handleFileUploadError,
                        'complete': self.handleFileUploadComplete
                    });
                }
            }
        });
    });
};

Teach.prototype.handleFileUploadProgress = function (response) {
    var total = response.total;
    var percent = total.percent;
    // console.log(percent);
    var percentText = percent.toFixed(0)+'%';
    // // 24.0909，89.000....
    // var progressGroup = News.progressGroup;
    var progressGroup = $('#progress-group');
    progressGroup.show();
    var progressBar = $(".progress-bar");
    progressBar.css({"width":percentText});
    progressBar.text(percentText);
};

Teach.prototype.handleFileUploadError = function (error) {
    window.messageBox.showError(error.message);
    var progressGroup = $("#progress-group");
    progressGroup.hide();
    console.log(error.message);
};

Teach.prototype.handleFileUploadComplete = function (response) {
    console.log(response);
    var progressGroup = $("#progress-group");
    progressGroup.hide();
    var domain = 'http://ps0j0p5j6.bkt.clouddn.com/';
    var filename = response.key;
    var url = domain + filename;
    var avatarInput = $("input[name='avatar']");
    avatarInput.val(url);
};

Teach.prototype.listenSubmitEvent = function () {
    var submitBtn = $("#submit-btn");
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-news-id');

        var username = $("input[name='username']").val();
        var avatar = $("input[name='avatar']").val();
        var jobtitle = $("input[name='jobtitle']").val();
        var profile = window.ue.getContent();
        // console.log(username);
        // console.log(avatar);
        // console.log(jobtitle);
        // console.log(content);
        var url = '';
        if(pk){
            url = '/course/edit_teach/';
        }else{
            url = '/course/teach/';
        }

        xfzajax.post({
            'url': url,
            'data': {
                'username': username,
                'avatar': avatar,
                'jobtitle': jobtitle,
                'profile': profile,
                'pk': pk
            },
            'success': function (result) {
                if(result['code'] === 200){
                    xfzalert.alertSuccess('恭喜！添加成功！',function () {
                        window.location.reload();
                    });
                }
            }
        });
    });
};

Teach.prototype.run = function () {
    var self = this;
    self.initUEditor();
    self.listenQiniuUploadFileEvent();
    self.listenSubmitEvent();
    // self.listenUploadFielEvent();
};

$(function () {
    var teach = new Teach();
    teach.run();
    Teach.progressGroup = $('#progress-group');
});