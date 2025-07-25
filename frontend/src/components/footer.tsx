const Footer = () => {
  return (
    <footer className="bg-primary text-white mt-auto">
      <div className="container mx-auto px-6 py-4">
        <div className="flex justify-center text-center">
          <p className="text-sm">
            © {new Date().getFullYear()} MoodMuse. All Rights Reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 