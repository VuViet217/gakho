from django.shortcuts import render
from django.http import HttpResponse


def custom_404(request, exception):
    """Custom 404 error page"""
    html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Không tìm thấy trang | GA Inventory</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }
        
        /* Animated background shapes */
        .shape {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            animation: float 20s infinite ease-in-out;
        }
        
        .shape:nth-child(1) {
            width: 60px;
            height: 60px;
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .shape:nth-child(2) {
            width: 90px;
            height: 90px;
            top: 60%;
            left: 80%;
            animation-delay: 2s;
        }
        
        .shape:nth-child(3) {
            width: 50px;
            height: 50px;
            top: 30%;
            left: 5%;
            animation-delay: 4s;
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
                opacity: 0.3;
            }
            50% {
                transform: translateY(-20px) rotate(180deg);
                opacity: 0.6;
            }
        }
        
        .error-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 35px 40px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 600px;
            width: 90%;
            max-height: 95vh;
            overflow-y: auto;
            animation: slideUp 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            z-index: 10;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .icon-wrapper {
            margin-bottom: 15px;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-15px);
            }
            60% {
                transform: translateY(-8px);
            }
        }
        
        .search-icon {
            width: 80px;
            height: 80px;
            margin: 0 auto;
            position: relative;
        }
        
        .search-circle {
            width: 55px;
            height: 55px;
            border: 6px solid #667eea;
            border-radius: 50%;
            position: absolute;
            top: 0;
            left: 13px;
            animation: pulse 2s infinite;
        }
        
        .search-handle {
            width: 6px;
            height: 32px;
            background: #764ba2;
            position: absolute;
            bottom: 0;
            right: 8px;
            transform: rotate(-45deg);
            border-radius: 3px;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
                opacity: 1;
            }
            50% {
                transform: scale(1.05);
                opacity: 0.8;
            }
        }
        
        .error-number {
            font-size: 90px;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            margin: 10px 0;
            letter-spacing: -3px;
        }
        
        .error-title {
            font-size: 26px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }
        
        .error-subtitle {
            font-size: 15px;
            color: #718096;
            margin-bottom: 20px;
            line-height: 1.5;
        }
        
        .error-code {
            display: inline-block;
            background: #f7fafc;
            border: 2px dashed #cbd5e0;
            padding: 8px 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #4a5568;
            margin-bottom: 20px;
        }
        
        .button-group {
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .btn {
            padding: 12px 28px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            border: none;
            cursor: pointer;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(102, 126, 234, 0.6);
        }
        
        .btn-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .btn-secondary:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(102, 126, 234, 0.4);
        }
        
        .helpful-links {
            padding-top: 20px;
            border-top: 2px solid #e2e8f0;
        }
        
        .helpful-links h3 {
            font-size: 14px;
            color: #4a5568;
            margin-bottom: 12px;
            font-weight: 600;
        }
        
        .links-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }
        
        .link-item {
            padding: 8px 12px;
            background: #f7fafc;
            border-radius: 8px;
            color: #667eea;
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .link-item:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .error-container {
                padding: 30px 25px;
            }
            .error-number {
                font-size: 70px;
            }
            .error-title {
                font-size: 22px;
            }
            .error-subtitle {
                font-size: 14px;
            }
            .button-group {
                flex-direction: column;
            }
            .btn {
                width: 100%;
                justify-content: center;
            }
            .links-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Custom scrollbar */
        .error-container::-webkit-scrollbar {
            width: 6px;
        }
        
        .error-container::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        .error-container::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
    
    <div class="error-container">
        <div class="icon-wrapper">
            <div class="search-icon">
                <div class="search-circle"></div>
                <div class="search-handle"></div>
            </div>
        </div>
        
        <div class="error-number">404</div>
        <h1 class="error-title">Không tìm thấy trang</h1>
        <p class="error-subtitle">
            Rất tiếc! Trang bạn đang tìm kiếm không tồn tại hoặc đã được di chuyển.
        </p>
        
        <div class="error-code">Error Code: HTTP 404 - Not Found</div>
        
        <div class="button-group">
            <a href="/vi/dashboard/" class="btn btn-primary">
                <span>🏠</span>
                <span>Về trang chủ</span>
            </a>
            <a href="javascript:history.back()" class="btn btn-secondary">
                <span>←</span>
                <span>Quay lại</span>
            </a>
        </div>
        
        <div class="helpful-links">
            <h3>📌 Liên kết hữu ích</h3>
            <div class="links-grid">
                <a href="/vi/dashboard/" class="link-item">Dashboard</a>
                <a href="/vi/inventory/" class="link-item">Kho hàng</a>
                <a href="/vi/procurement/suppliers/" class="link-item">Nhà cung cấp</a>
                <a href="/vi/hr/employees/" class="link-item">Nhân viên</a>
            </div>
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            document.addEventListener('mousemove', function(e) {
                const shapes = document.querySelectorAll('.shape');
                const x = e.clientX / window.innerWidth;
                const y = e.clientY / window.innerHeight;
                
                shapes.forEach((shape, index) => {
                    const speed = (index + 1) * 15;
                    const xMove = (x - 0.5) * speed;
                    const yMove = (y - 0.5) * speed;
                    shape.style.transform = `translate(${xMove}px, ${yMove}px)`;
                });
            });
        });
    </script>
</body>
</html>
    """
    return HttpResponse(html, status=404)
    """Custom 404 error page"""
    html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Không tìm thấy trang | GA Inventory</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }
        
        /* Animated background shapes */
        .shape {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            animation: float 20s infinite ease-in-out;
        }
        
        .shape:nth-child(1) {
            width: 80px;
            height: 80px;
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .shape:nth-child(2) {
            width: 120px;
            height: 120px;
            top: 70%;
            left: 80%;
            animation-delay: 2s;
        }
        
        .shape:nth-child(3) {
            width: 60px;
            height: 60px;
            top: 40%;
            left: 5%;
            animation-delay: 4s;
        }
        
        .shape:nth-child(4) {
            width: 100px;
            height: 100px;
            top: 20%;
            left: 85%;
            animation-delay: 1s;
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
                opacity: 0.3;
            }
            50% {
                transform: translateY(-30px) rotate(180deg);
                opacity: 0.6;
            }
        }
        
        .error-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 60px 50px;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 650px;
            width: 90%;
            animation: slideUp 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            z-index: 10;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(50px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .icon-wrapper {
            margin-bottom: 30px;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-20px);
            }
            60% {
                transform: translateY(-10px);
            }
        }
        
        .search-icon {
            width: 120px;
            height: 120px;
            margin: 0 auto;
            position: relative;
        }
        
        .search-circle {
            width: 80px;
            height: 80px;
            border: 8px solid #667eea;
            border-radius: 50%;
            position: absolute;
            top: 0;
            left: 20px;
            animation: pulse 2s infinite;
        }
        
        .search-handle {
            width: 8px;
            height: 45px;
            background: #764ba2;
            position: absolute;
            bottom: 0;
            right: 10px;
            transform: rotate(-45deg);
            border-radius: 4px;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
                opacity: 1;
            }
            50% {
                transform: scale(1.05);
                opacity: 0.8;
            }
        }
        
        .error-number {
            font-size: 140px;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            margin: 20px 0;
            letter-spacing: -5px;
            text-shadow: 0 5px 25px rgba(102, 126, 234, 0.3);
            animation: glitch 3s infinite;
        }
        
        @keyframes glitch {
            0%, 90%, 100% {
                transform: translate(0);
            }
            92%, 96% {
                transform: translate(-2px, 2px);
            }
            94%, 98% {
                transform: translate(2px, -2px);
            }
        }
        
        .error-title {
            font-size: 36px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 15px;
            letter-spacing: -0.5px;
        }
        
        .error-subtitle {
            font-size: 18px;
            color: #718096;
            margin-bottom: 35px;
            line-height: 1.7;
        }
        
        .error-code {
            display: inline-block;
            background: #f7fafc;
            border: 2px dashed #cbd5e0;
            padding: 12px 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: #4a5568;
            margin-bottom: 30px;
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 16px 36px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            border: none;
            cursor: pointer;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        }
        
        .btn-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .btn-secondary:hover {
            background: #667eea;
            color: white;
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .helpful-links {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #e2e8f0;
        }
        
        .helpful-links h3 {
            font-size: 16px;
            color: #4a5568;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .links-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
            margin-top: 15px;
        }
        
        .link-item {
            padding: 10px 15px;
            background: #f7fafc;
            border-radius: 10px;
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .link-item:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .error-container {
                padding: 40px 30px;
            }
            .error-number {
                font-size: 100px;
            }
            .error-title {
                font-size: 28px;
            }
            .error-subtitle {
                font-size: 16px;
            }
            .button-group {
                flex-direction: column;
            }
            .btn {
                width: 100%;
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
    
    <div class="error-container">
        <div class="icon-wrapper">
            <div class="search-icon">
                <div class="search-circle"></div>
                <div class="search-handle"></div>
            </div>
        </div>
        
        <div class="error-number">404</div>
        <h1 class="error-title">Không tìm thấy trang</h1>
        <p class="error-subtitle">
            Rất tiếc! Trang bạn đang tìm kiếm không tồn tại hoặc đã được di chuyển.<br>
            Vui lòng kiểm tra lại URL hoặc quay về trang chủ.
        </p>
        
        <div class="error-code">Error Code: HTTP 404 - Not Found</div>
        
        <div class="button-group">
            <a href="/vi/dashboard/" class="btn btn-primary">
                <span>🏠</span>
                <span>Về trang chủ</span>
            </a>
            <a href="javascript:history.back()" class="btn btn-secondary">
                <span>←</span>
                <span>Quay lại</span>
            </a>
        </div>
        
        <div class="helpful-links">
            <h3>📌 Liên kết hữu ích</h3>
            <div class="links-grid">
                <a href="/vi/dashboard/" class="link-item">Dashboard</a>
                <a href="/vi/inventory/" class="link-item">Kho hàng</a>
                <a href="/vi/procurement/suppliers/" class="link-item">Nhà cung cấp</a>
                <a href="/vi/hr/employees/" class="link-item">Nhân viên</a>
            </div>
        </div>
    </div>
    
    <script>
        // Add some interactivity
        document.addEventListener('DOMContentLoaded', function() {
            // Add mouse move effect to shapes
            document.addEventListener('mousemove', function(e) {
                const shapes = document.querySelectorAll('.shape');
                const x = e.clientX / window.innerWidth;
                const y = e.clientY / window.innerHeight;
                
                shapes.forEach((shape, index) => {
                    const speed = (index + 1) * 20;
                    const xMove = (x - 0.5) * speed;
                    const yMove = (y - 0.5) * speed;
                    shape.style.transform = `translate(${xMove}px, ${yMove}px)`;
                });
            });
        });
    </script>
</body>
</html>
    """
    return HttpResponse(html, status=404)


def custom_500(request):
    """Custom 500 error page"""
    html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>500 - Lỗi máy chủ | GA Inventory</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }
        
        .shape {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            animation: float 20s infinite ease-in-out;
        }
        
        .shape:nth-child(1) {
            width: 60px;
            height: 60px;
            top: 15%;
            left: 15%;
            animation-delay: 0s;
        }
        
        .shape:nth-child(2) {
            width: 80px;
            height: 80px;
            top: 65%;
            left: 75%;
            animation-delay: 2s;
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
                opacity: 0.3;
            }
            50% {
                transform: translateY(-20px) rotate(180deg);
                opacity: 0.6;
            }
        }
        
        .error-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 35px 40px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 600px;
            width: 90%;
            max-height: 95vh;
            overflow-y: auto;
            animation: shake 0.6s;
            position: relative;
            z-index: 10;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-3px); }
            20%, 40%, 60%, 80% { transform: translateX(3px); }
        }
        
        .icon-wrapper {
            margin-bottom: 15px;
            animation: buzz 0.5s infinite;
        }
        
        @keyframes buzz {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-3deg); }
            75% { transform: rotate(3deg); }
        }
        
        .warning-icon {
            width: 80px;
            height: 80px;
            margin: 0 auto;
            position: relative;
        }
        
        .triangle {
            width: 0;
            height: 0;
            border-left: 40px solid transparent;
            border-right: 40px solid transparent;
            border-bottom: 70px solid #fc4a1a;
            position: relative;
            animation: pulse 2s infinite;
        }
        
        .exclamation {
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 35px;
            font-weight: bold;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
                opacity: 1;
            }
            50% {
                transform: scale(1.05);
                opacity: 0.9;
            }
        }
        
        .error-number {
            font-size: 90px;
            font-weight: 900;
            background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            margin: 10px 0;
            letter-spacing: -3px;
        }
        
        .error-title {
            font-size: 26px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        .error-subtitle {
            font-size: 15px;
            color: #718096;
            margin-bottom: 20px;
            line-height: 1.5;
        }
        
        .error-details {
            background: #fff5f5;
            border-left: 4px solid #fc4a1a;
            padding: 12px 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: left;
        }
        
        .error-details h4 {
            color: #fc4a1a;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 6px;
        }
        
        .error-details p {
            color: #718096;
            font-size: 13px;
            line-height: 1.4;
        }
        
        .button-group {
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 28px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
            color: white;
            box-shadow: 0 8px 20px rgba(252, 74, 26, 0.4);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(252, 74, 26, 0.6);
        }
        
        .btn-secondary {
            background: white;
            color: #fc4a1a;
            border: 2px solid #fc4a1a;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .btn-secondary:hover {
            background: #fc4a1a;
            color: white;
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .error-container {
                padding: 30px 25px;
            }
            .error-number {
                font-size: 70px;
            }
            .error-title {
                font-size: 22px;
            }
            .button-group {
                flex-direction: column;
            }
            .btn {
                width: 100%;
                justify-content: center;
            }
        }
        
        .error-container::-webkit-scrollbar {
            width: 6px;
        }
        
        .error-container::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        .error-container::-webkit-scrollbar-thumb {
            background: #fc4a1a;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="shape"></div>
    <div class="shape"></div>
    
    <div class="error-container">
        <div class="icon-wrapper">
            <div class="warning-icon">
                <div class="triangle">
                    <div class="exclamation">!</div>
                </div>
            </div>
        </div>
        
        <div class="error-number">500</div>
        <h1 class="error-title">Lỗi máy chủ nội bộ</h1>
        <p class="error-subtitle">
            Rất tiếc! Đã xảy ra lỗi trên máy chủ của chúng tôi.<br>
            Nhóm kỹ thuật đã được thông báo và đang khắc phục sự cố.
        </p>
        
        <div class="error-details">
            <h4>🔧 Đang xử lý</h4>
            <p>Lỗi này đã được ghi nhận. Vui lòng thử lại sau vài phút hoặc liên hệ bộ phận hỗ trợ nếu sự cố vẫn tiếp diễn.</p>
        </div>
        
        <div class="button-group">
            <a href="/vi/dashboard/" class="btn btn-primary">
                <span>🏠</span>
                <span>Về trang chủ</span>
            </a>
            <a href="javascript:location.reload()" class="btn btn-secondary">
                <span>🔄</span>
                <span>Thử lại</span>
            </a>
        </div>
    </div>
    
    <script>
        document.addEventListener('mousemove', function(e) {
            const shapes = document.querySelectorAll('.shape');
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            shapes.forEach((shape, index) => {
                const speed = (index + 1) * 15;
                const xMove = (x - 0.5) * speed;
                const yMove = (y - 0.5) * speed;
                shape.style.transform = `translate(${xMove}px, ${yMove}px)`;
            });
        });
    </script>
</body>
</html>
    """
    return HttpResponse(html, status=500)
    """Custom 500 error page"""
    html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>500 - Lỗi máy chủ | GA Inventory</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }
        
        .shape {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            animation: float 20s infinite ease-in-out;
        }
        
        .shape:nth-child(1) {
            width: 80px;
            height: 80px;
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .shape:nth-child(2) {
            width: 120px;
            height: 120px;
            top: 70%;
            left: 80%;
            animation-delay: 2s;
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
                opacity: 0.3;
            }
            50% {
                transform: translateY(-30px) rotate(180deg);
                opacity: 0.6;
            }
        }
        
        .error-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 60px 50px;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 650px;
            width: 90%;
            animation: shake 0.8s;
            position: relative;
            z-index: 10;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        .icon-wrapper {
            margin-bottom: 30px;
            animation: buzz 0.5s infinite;
        }
        
        @keyframes buzz {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-5deg); }
            75% { transform: rotate(5deg); }
        }
        
        .warning-icon {
            width: 120px;
            height: 120px;
            margin: 0 auto;
            position: relative;
        }
        
        .triangle {
            width: 0;
            height: 0;
            border-left: 60px solid transparent;
            border-right: 60px solid transparent;
            border-bottom: 100px solid #fc4a1a;
            position: relative;
            animation: pulse 2s infinite;
        }
        
        .exclamation {
            position: absolute;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 50px;
            font-weight: bold;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
                opacity: 1;
            }
            50% {
                transform: scale(1.05);
                opacity: 0.9;
            }
        }
        
        .error-number {
            font-size: 140px;
            font-weight: 900;
            background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            margin: 20px 0;
            letter-spacing: -5px;
        }
        
        .error-title {
            font-size: 36px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 15px;
        }
        
        .error-subtitle {
            font-size: 18px;
            color: #718096;
            margin-bottom: 35px;
            line-height: 1.7;
        }
        
        .error-details {
            background: #fff5f5;
            border-left: 4px solid #fc4a1a;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: left;
        }
        
        .error-details h4 {
            color: #fc4a1a;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .error-details p {
            color: #718096;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 16px 36px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
            color: white;
            box-shadow: 0 10px 30px rgba(252, 74, 26, 0.4);
        }
        
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(252, 74, 26, 0.6);
        }
        
        .btn-secondary {
            background: white;
            color: #fc4a1a;
            border: 2px solid #fc4a1a;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .btn-secondary:hover {
            background: #fc4a1a;
            color: white;
            transform: translateY(-3px);
        }
        
        @media (max-width: 768px) {
            .error-container {
                padding: 40px 30px;
            }
            .error-number {
                font-size: 100px;
            }
            .error-title {
                font-size: 28px;
            }
            .button-group {
                flex-direction: column;
            }
            .btn {
                width: 100%;
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="shape"></div>
    <div class="shape"></div>
    
    <div class="error-container">
        <div class="icon-wrapper">
            <div class="warning-icon">
                <div class="triangle">
                    <div class="exclamation">!</div>
                </div>
            </div>
        </div>
        
        <div class="error-number">500</div>
        <h1 class="error-title">Lỗi máy chủ nội bộ</h1>
        <p class="error-subtitle">
            Rất tiếc! Đã xảy ra lỗi trên máy chủ của chúng tôi.<br>
            Nhóm kỹ thuật đã được thông báo và đang khắc phục sự cố.
        </p>
        
        <div class="error-details">
            <h4>🔧 Đang xử lý</h4>
            <p>Lỗi này đã được ghi nhận. Vui lòng thử lại sau vài phút hoặc liên hệ bộ phận hỗ trợ nếu sự cố vẫn tiếp diễn.</p>
        </div>
        
        <div class="button-group">
            <a href="/vi/dashboard/" class="btn btn-primary">
                <span>🏠</span>
                <span>Về trang chủ</span>
            </a>
            <a href="javascript:location.reload()" class="btn btn-secondary">
                <span>🔄</span>
                <span>Thử lại</span>
            </a>
        </div>
    </div>
    
    <script>
        document.addEventListener('mousemove', function(e) {
            const shapes = document.querySelectorAll('.shape');
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            shapes.forEach((shape, index) => {
                const speed = (index + 1) * 20;
                const xMove = (x - 0.5) * speed;
                const yMove = (y - 0.5) * speed;
                shape.style.transform = `translate(${xMove}px, ${yMove}px)`;
            });
        });
    </script>
</body>
</html>
    """
    return HttpResponse(html, status=500)
