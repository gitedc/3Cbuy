class UrlRecordMiddleware(object):


    exclude_path = ['/user/login/','/user/regiester/',
                    '/user/register_check/','/user/logout/','/user/login_check/']
    def process_view(self,request,view_func,*view_args,**view_kwargs):
        # print('--------%s------'%request.path)
        # request.get_full_path()
        print(request.path)
        if request.path not in UrlRecordMiddleware.exclude_path:
            request.session['pre_url_path'] = request.get_full_path()