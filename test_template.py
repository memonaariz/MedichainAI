from app import app
with app.test_request_context():
    from flask import render_template
    try:
        r = render_template('doctor/messages.html',
            user={'name':'Dr Test','role':'doctor','username':'doctor1'},
            messages=[])
        print('RENDER OK', len(r), 'chars')
        if len(r) > 100:
            print('First 200 chars:', r[:200])
    except Exception as e:
        import traceback
        print('RENDER ERROR:', e)
        traceback.print_exc()
