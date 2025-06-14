export default function Record() {
    return (<div className="min-h-screen  flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-lg p-8 sm:p-8 max-w-md w-full text-center">

            <div className="mb-8">
                <div className="w-28 h-28 sm:w-32 sm:h-32 mx-auto bg-green-600 rounded-full flex items-center justify-center">                        
                    <svg
                    className="w-14 h-14 sm:w-16 sm:h-16 text-white"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path d="M20 2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM8 20H4V4h4v16zm2-8c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2zm8 8h-4V4h4v16z" />
                    <circle cx="12" cy="12" r="2" />
                </svg>
                </div>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold text-green-600 mb-6">
                NFC Scanner
            </h1>


            <p className="text-base sm:text-lg text-gray-700 mb-8">
                Please scan your NFC card
            </p>
            <div className="flex items-center justify-center space-x-2 p-4 bg-green-50 rounded-lg border border-green-200">
                <div className="w-3 h-3 bg-green-600 rounded-full animate-pulse"></div>
                <span className="text-green-600 text-base font-medium">Ready to scan</span>
            </div>
        </div>
    </div>
    );
}