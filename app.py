
import os
import sys
import threading
from flask import Flask, render_template, request, jsonify
from psycopg2.extras import RealDictCursor

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from unified_resume_platform.backend.integrations.hr_integration import HRIntegration
    from unified_resume_platform.backend.integrations.jobseeker_integration import JobSeekerIntegration
except ImportError as e:
    print(f"Error importing backend modules: {e}")
    print(f"Current directory: {current_dir}")
    print(f"Python path: {sys.path}")
    raise

template_folder = os.path.join(current_dir, 'unified_resume_platform', 'frontend', 'templates')
static_folder = os.path.join(current_dir, 'unified_resume_platform', 'frontend', 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config['SECRET_KEY'] = 'unified-resume-platform-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

hr_integration = HRIntegration()
jobseeker_integration = JobSeekerIntegration()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hr')
def hr_dashboard():
    return render_template('hr_dashboard.html')

@app.route('/jobseeker')
def jobseeker_dashboard():
    try:
        # Load existing profile if available
        profile_result = jobseeker_integration.get_profile()
        profile = profile_result['data'] if profile_result['success'] else None
        return render_template('jobseeker_dashboard.html', profile=profile)
    except Exception as e:
        print(f"Error loading profile for dashboard: {e}")
        return render_template('jobseeker_dashboard.html', profile=None)

@app.route('/api/hr/match', methods=['POST'])
def hr_match():
    try:
        data = request.get_json()
        result = hr_integration.analyze_match(
            data.get('resume', ''),
            data.get('job_description', '')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/hr/rank', methods=['POST'])
def hr_rank():
    try:
        data = request.get_json()
        result = hr_integration.rank_candidates(data.get('job_description', ''))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/hr/samples')
def hr_samples():
    try:
        result = hr_integration.get_sample_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/hr/sample/<sample_type>/<name>')
def hr_sample_content(sample_type, name):
    try:
        result = hr_integration.get_sample_content(sample_type, name)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/test-db')
def test_database():
    """Test database connection and data for debugging"""
    try:
        from unified_resume_platform.backend.database.db_manager import DatabaseManager
        db_manager = DatabaseManager()
        
        if db_manager.connect():
            cursor = db_manager.connection.cursor(cursor_factory=RealDictCursor)

            # Test resumes table
            cursor.execute("SELECT COUNT(*) as count FROM resumes")
            resume_count = cursor.fetchone()['count']
            
            # Test job_descriptions table  
            cursor.execute("SELECT COUNT(*) as count FROM job_descriptions")
            job_count = cursor.fetchone()['count']
            
            # Get sample data
            cursor.execute("SELECT resume_id, resume_title, candidate_name FROM resumes LIMIT 3")
            sample_resumes = cursor.fetchall()
            
            cursor.execute("SELECT job_id, job_title, company_name FROM job_descriptions LIMIT 3")
            sample_jobs = cursor.fetchall()
            
            cursor.close()
            db_manager.disconnect()
            
            return jsonify({
                'success': True,
                'message': 'Database connection successful',
                'data': {
                    'resume_count': resume_count,
                    'job_count': job_count,
                    'sample_resumes': sample_resumes,
                    'sample_jobs': sample_jobs
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to connect to database - check password in db_config.py'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Database error: {str(e)}'
        })

@app.route('/api/jobseeker/profiles', methods=['GET'])
def jobseeker_list_profiles():
    try:
        return jsonify(jobseeker_integration.list_profiles())
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/jobseeker/profile', methods=['GET'])
def jobseeker_get_profile():
    try:
        result = jobseeker_integration.get_profile(request.args.get('name'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/jobseeker/profile', methods=['POST', 'PUT'])
def jobseeker_save_profile():
    try:
        data = request.get_json()
        if request.method == 'POST':
            result = jobseeker_integration.create_profile(data)
        else:
            result = jobseeker_integration.update_profile(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/jobseeker/validate', methods=['POST'])
def jobseeker_validate():
    try:
        data = request.get_json()
        result = jobseeker_integration.validate_profile(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/jobseeker/analyze', methods=['POST'])
def jobseeker_analyze():
    try:
        data = request.get_json()
        result = jobseeker_integration.analyze_job(data.get('job_description', ''))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/jobseeker/generate', methods=['POST'])
def jobseeker_generate():
    try:
        data = request.get_json()
        result = jobseeker_integration.generate_resume(
            data.get('profile'),
            data.get('analysis')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/jobseeker/export', methods=['POST'])
def jobseeker_export():
    """Export resume in specified format and trigger download"""
    try:
        data = request.get_json()
        result = jobseeker_integration.export_resume(
            data.get('content'),
            data.get('format'),
            data.get('profile'),
            data.get('job_description'),
            data.get('resume_data')
        )
        
        if result['success'] and 'file_data' in result['data']:
            # Return file for download with proper headers
            from flask import make_response
            
            file_data = result['data']['file_data']
            filename = result['data']['filename']
            content_type = result['data']['content_type']
            
            # Create response with binary data
            response = make_response(file_data)
            response.headers['Content-Type'] = content_type
            response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
            response.headers['Content-Length'] = len(file_data)
            
            # Add cache control headers
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            
            return response
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(_error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(_error):
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

def check_database_connection():
    """Check database connection and display status on startup"""
    try:
        from unified_resume_platform.backend.database.db_config import test_connection
        from unified_resume_platform.backend.database.db_manager import DatabaseManager
        
        print("\n" + "="*60)
        print("DATABASE CONNECTION CHECK")
        print("="*60)
        
        # Test basic connection
        if test_connection():
            # Test data availability
            db_manager = DatabaseManager()
            if db_manager.connect():
                cursor = db_manager.connection.cursor(cursor_factory=RealDictCursor)

                # Check resumes table
                cursor.execute("SELECT COUNT(*) as count FROM resumes")
                resume_count = cursor.fetchone()['count']
                
                # Check job_descriptions table
                cursor.execute("SELECT COUNT(*) as count FROM job_descriptions")
                job_count = cursor.fetchone()['count']
                
                cursor.close()
                db_manager.disconnect()
                
                print(f"✓ Database: unified_resume_portal")
                print(f"✓ Resumes available: {resume_count}")
                print(f"✓ Job descriptions available: {job_count}")
                
                if resume_count > 0 and job_count > 0:
                    print("✓ Sample data loaded successfully")
                    print("✓ HR dropdowns will be populated")
                else:
                    print("⚠ No sample data found")
                    print("⚠ Please run insert_data.sql to populate database")
                
                return True
            else:
                print("✗ Failed to connect to database")
                return False
        else:
            print("✗ Database connection failed")
            print("\nTo fix this:")
            print("1. Make sure SUPABASE_DB_URL is set in your .env file")
            print("2. Make sure your Supabase project is not paused")
            print("3. Run supabase_schema.sql and insert_data.sql in the Supabase SQL Editor")
            print("4. If connecting fails on a home network, use the Session Pooler URI")
            return False
            
    except Exception as e:
        print(f"✗ Database check error: {e}")
        print("\nApplication will continue but database features may not work")
        return False
    finally:
        print("="*60 + "\n")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("ResuMatch AI")
    print("="*50)
    
    # Check database connection on startup
    db_status = check_database_connection()
    
    print("Server: http://localhost:5000")
    if db_status:
        print("Status: Ready with database")
    else:
        print("Status: Running without database (limited functionality)")
    print("="*50 + "\n")

    # Warm up the semantic model in the background (only in the process that
    # actually serves requests) so the first analysis/ranking isn't slow.
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        def _prewarm_model():
            try:
                from unified_resume_platform.backend.models.matching_engine import _get_embedding_model
                _get_embedding_model()
            except Exception as e:
                print(f"Model prewarm skipped: {e}")
        threading.Thread(target=_prewarm_model, daemon=True).start()

    # Exclude site-packages so the reloader doesn't restart on lazy imports of
    # large ML libraries (transformers/torch/spaCy), which breaks in-flight requests.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, exclude_patterns=['*site-packages*'])
