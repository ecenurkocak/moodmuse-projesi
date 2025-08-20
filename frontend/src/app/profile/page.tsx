"use client";

import { useState, useEffect } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/context/AuthContext';
import { updateUserProfile, uploadProfileImage } from '@/services/api';
import { Loader2, CheckCircle, AlertTriangle, Upload, KeyRound, QrCode, Laptop, Smartphone } from 'lucide-react';
import { Switch } from '@/components/ui/switch';
import { Checkbox } from '@/components/ui/checkbox';

const ProfilePage = () => {
  const router = useRouter();
  const { user, fetchUser } = useAuth();

  const [displayName, setDisplayName] = useState('');
  const [bio, setBio] = useState('');
  
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [profileImage, setProfileImage] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const [language, setLanguage] = useState('TR');
  const [theme, setTheme] = useState('Otomatik'); 
  
  const [dailyReminder, setDailyReminder] = useState('09:00');
  const [weeklySummary, setWeeklySummary] = useState(true);

  // Bildirim State'leri
  const [socialFollow, setSocialFollow] = useState(true);
  const [socialFollowEmail, setSocialFollowEmail] = useState(true);
  const [socialFollowPush, setSocialFollowPush] = useState(false);

  const [socialComment, setSocialComment] = useState(true);
  const [socialCommentEmail, setSocialCommentEmail] = useState(true);
  const [socialCommentPush, setSocialCommentPush] = useState(true);

  const [appUpdates, setAppUpdates] = useState(true);
  const [appUpdatesEmail, setAppUpdatesEmail] = useState(true);
  const [appUpdatesPush, setAppUpdatesPush] = useState(true);

  const [appWeeklySummary, setAppWeeklySummary] = useState(false);
  const [appWeeklySummaryEmail, setAppWeeklySummaryEmail] = useState(false);
  const [appWeeklySummaryPush, setAppWeeklySummaryPush] = useState(false);

  // Güvenlik State'leri
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');


  const [spotifyConnected, setSpotifyConnected] = useState(false);

  const [shareData, setShareData] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
    }
  }, [router]);

  useEffect(() => {
    if (user) {
      setDisplayName(user.username || '');
    }
  }, [user]);

  const handleImageChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setProfileImage(file);
      setIsUploading(true);
      setError(null);
      setSuccessMessage(null);
      
      try {
        await uploadProfileImage(file);
        setSuccessMessage('Profil fotoğrafı başarıyla yüklendi!');
        if (fetchUser) {
          await fetchUser(); // Kullanıcı bilgilerini ve yeni fotoğrafı çek
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Fotoğraf yüklenirken bir hata oluştu.');
      } finally {
        setIsUploading(false);
      }
    }
  };

  const handleProfileUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setSuccessMessage(null);
    setError(null);

    try {
      const updatedData = {
        username: displayName,
        bio: bio,
      };
      await updateUserProfile(updatedData);
      setSuccessMessage('Profil başarıyla güncellendi!');
      
      if (fetchUser) {
        await fetchUser();
      }

    } catch (err: any) {
      setError(err.response?.data?.detail || 'Profil güncellenirken bir hata oluştu.');
    } finally {
      setIsLoading(false);
    }
  };
  
  if (!user) {
      return (
          <div className="flex items-center justify-center h-screen bg-bg-main">
                <div className="text-2xl text-text-main">Yükleniyor...</div>
          </div>
      )
  }

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-text-main">
      <h1 className="text-4xl font-bold text-center my-10">Profile Settings</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        
        <div className="md:col-span-1">
            <div className="bg-white/10 backdrop-blur-md p-6 rounded-xl shadow-lg border border-white/20 text-center">
                <div className="relative group w-24 h-24 mx-auto mb-4">
                    <div className="w-full h-full rounded-full bg-white/10 flex items-center justify-center border-2 border-primary overflow-hidden">
                        {isUploading ? (
                          <Loader2 className="w-8 h-8 text-primary animate-spin" />
                        ) : user?.profile_image_url ? (
                          <Image
                            src={`${process.env.NEXT_PUBLIC_API_URL}${user.profile_image_url}`}
                            alt="Profile Picture"
                            width={96}
                            height={96}
                            className="object-cover w-full h-full"
                          />
                        ) : (
                          <span className="text-4xl font-bold text-primary">{displayName.charAt(0).toUpperCase()}</span>
                        )}
                    </div>
                    <label 
                        htmlFor="profile-picture-upload"
                        className="absolute inset-0 flex flex-col items-center justify-center bg-black bg-opacity-60 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300 cursor-pointer"
                    >
                        <Upload className="w-6 h-6 text-white mb-1" />
                        <span className="text-white text-xs text-center">Image<br/>Change</span>
                    </label>
                    <input 
                        type="file" 
                        id="profile-picture-upload" 
                        className="hidden" 
                        accept="image/*" 
                        onChange={handleImageChange} 
                        disabled={isUploading}
                    />
                </div>
                <h2 className="text-2xl font-semibold text-text-main">@{displayName}</h2>
                <p className="text-sm text-text-secondary mt-1">Member Since: {new Date(user.created_at).toLocaleDateString()}</p>
            </div>
        </div>

        <div className="md:col-span-2 space-y-8">
          
          <form onSubmit={handleProfileUpdate} className="bg-white/10 backdrop-blur-md p-6 rounded-xl shadow-lg border border-white/20">
            <h2 className="text-2xl font-bold mb-4 text-text-main">Account Information</h2>
            
            {error && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-md mb-4 flex items-center">
                <AlertTriangle className="mr-2" size={20} />
                <span>{error}</span>
              </div>
            )}
            {successMessage && (
              <div className="bg-green-500/10 border border-green-500/20 text-green-400 px-4 py-3 rounded-md mb-4 flex items-center">
                <CheckCircle className="mr-2" size={20} />
                <span>{successMessage}</span>
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label htmlFor="displayName" className="block text-sm font-medium text-text-secondary mb-1">Display Name</label>
                <input id="displayName" type="text" value={displayName} onChange={(e) => setDisplayName(e.target.value)} className="w-full p-2 bg-white/10 border border-white/30 rounded-md text-text-main focus:ring-primary focus:border-primary"/>
              </div>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-text-secondary mb-1">Email Address</label>
                <div className="flex items-center space-x-2">
                  <input id="email" type="email" value={user.email} disabled className="w-full p-2 bg-white/5 border border-white/20 rounded-md text-text-secondary cursor-not-allowed"/>
                  <Button type="button" variant="outline" className="text-white">Edit</Button>
                </div>
              </div>
              <div>
                <label htmlFor="bio" className="block text-sm font-medium text-text-secondary mb-1">About Me</label>
                <textarea id="bio" value={bio} onChange={(e) => setBio(e.target.value)} className="w-full p-2 h-24 bg-white/10 border border-white/30 rounded-md text-text-main focus:ring-primary focus:border-primary" placeholder="Tell something about yourself..."></textarea>
              </div>
              <Button type="submit" disabled={isLoading} className="flex items-center justify-center text-white">
                {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                {isLoading ? 'Kaydediliyor...' : 'Save Changes'}
              </Button>
            </div>
          </form>

          <div className="bg-white/10 backdrop-blur-md p-6 rounded-xl shadow-lg border border-white/20">
            <h2 className="text-2xl font-bold mb-6 text-text-main">Preferences</h2>
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Language</label>
                <div className="flex flex-wrap gap-2">
                  <Button variant={language === 'TR' ? 'default' : 'outline'} onClick={() => setLanguage('TR')} className="text-white">Turkish</Button>
                  <Button variant={language === 'EN' ? 'default' : 'outline'} onClick={() => setLanguage('EN')} className="text-white">English</Button>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Theme</label>
                <div className="flex flex-wrap gap-2">
                  <Button variant={theme === 'Otomatik' ? 'default' : 'outline'} onClick={() => setTheme('Otomatik')} className="text-white">System Default</Button>
                  <Button variant={theme === 'Aydınlık' ? 'default' : 'outline'} onClick={() => setTheme('Aydınlık')} className="text-white">Light</Button>
                  <Button variant={theme === 'Karanlık' ? 'default' : 'outline'} onClick={() => setTheme('Karanlık')} className="text-white">Dark</Button>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md p-6 rounded-xl shadow-lg border border-white/20">
            <h2 className="text-2xl font-bold mb-6 text-text-main">Notifications</h2>
            <div className="space-y-8">
             {/* Uygulama ve Güncellemeler */}
              <div>
                <h3 className="text-lg font-semibold text-text-main mb-4">App & Updates</h3>
                <div className="space-y-4">
                  <NotificationSetting
                    label="New features and announcements"
                    enabled={appUpdates}
                    onEnabledChange={setAppUpdates}
                    emailEnabled={appUpdatesEmail}
                    onEmailChange={setAppUpdatesEmail}
                    pushEnabled={appUpdatesPush}
                    onPushChange={setAppUpdatesPush}
                  />
                  <NotificationSetting
                    label="Weekly activity summary"
                    enabled={appWeeklySummary}
                    onEnabledChange={setAppWeeklySummary}
                    emailEnabled={appWeeklySummaryEmail}
                    onEmailChange={setAppWeeklySummaryEmail}
                    pushEnabled={appWeeklySummaryPush}
                    onPushChange={setAppWeeklySummaryPush}
                  />
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white/10 backdrop-blur-md p-6 rounded-xl shadow-lg border border-white/20">
            <h2 className="text-2xl font-bold mb-6 text-text-main">Security</h2>
            <div className="space-y-8">
              {/* Parola Değiştir */}
              <div>
                <h3 className="text-lg font-semibold text-text-main mb-4 flex items-center">
                    <KeyRound className="mr-2" /> Change Password
                </h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-1">Current Password</label>
                    <input type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} className="w-full p-2 bg-white/10 border border-white/30 rounded-md text-text-main focus:ring-primary focus:border-primary" placeholder="••••••••" />
                  </div>
                    <div>
                      <label className="block text-sm font-medium text-text-secondary mb-1">Yeni Parola</label>
                    <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} className="w-full p-2 bg-white/10 border border-white/30 rounded-md text-text-main focus:ring-primary focus:border-primary" placeholder="Enter your new password" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-1">Confirm New Password</label>
                    <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="w-full p-2 bg-white/10 border border-white/30 rounded-md text-text-main focus:ring-primary focus:border-primary" placeholder="Re-enter your new password" />
                  </div>
                  <Button className="text-white">Update Password</Button>
                </div>
              </div>

              {/* İki Faktörlü Kimlik Doğrulama */}
              <div>
                <h3 className="text-lg font-semibold text-text-main mb-4 flex items-center">
                  <QrCode className="mr-2" /> Two-Factor Authentication (2FA)
                </h3>
                <div className="p-4 rounded-lg bg-white/5 flex flex-col sm:flex-row items-start sm:items-center justify-between">
                  <div className="mb-3 sm:mb-0">
                    <p className="text-sm text-text-secondary">Status: <span className="font-semibold text-yellow-400">Not Active</span></p>
                  </div>
                  <Button variant="outline" className="text-white">Enable</Button>
                </div>
              </div>

              {/* Aktif Oturumlar */}
              <div>
                <h3 className="text-lg font-semibold text-text-main mb-4">Active Sessions</h3>
                <div className="space-y-4">
                  <div className="p-4 rounded-lg bg-white/5 flex items-center justify-between">
                    <div className="flex items-center">
                      <Laptop className="w-6 h-6 mr-4 text-text-secondary" />
                      <div>
                        <p className="text-text-main">Chrome - İstanbul, Türkiye</p>
                        <p className="text-sm text-green-400 font-semibold">Current session</p>
                      </div>
                    </div>
                    <Button variant="destructive" size="sm">Log out</Button>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

// Tekrarlanan bildirim ayarı satırları için yardımcı bileşen
interface NotificationSettingProps {
  label: string;
  enabled: boolean;
  onEnabledChange: (enabled: boolean) => void;
  emailEnabled: boolean;
  onEmailChange: (enabled: boolean) => void;
  pushEnabled: boolean;
  onPushChange: (enabled: boolean) => void;
}

const NotificationSetting: React.FC<NotificationSettingProps> = ({
  label,
  enabled,
  onEnabledChange,
  emailEnabled,
  onEmailChange,
  pushEnabled,
  onPushChange,
}) => (
  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 rounded-lg bg-white/5">
    <span className="text-text-main mb-3 sm:mb-0">{label}</span>
    <div className="flex items-center space-x-6">
      <div className="flex items-center space-x-2">
        <Checkbox checked={emailEnabled} onCheckedChange={onEmailChange} id={`email-${label}`} disabled={!enabled} />
        <label htmlFor={`email-${label}`} className="text-sm text-text-secondary cursor-pointer">E-posta</label>
      </div>
      <div className="flex items-center space-x-2">
        <Checkbox checked={pushEnabled} onCheckedChange={onPushChange} id={`push-${label}`} disabled={!enabled} />
        <label htmlFor={`push-${label}`} className="text-sm text-text-secondary cursor-pointer">Anlık</label>
      </div>
      <Switch checked={enabled} onCheckedChange={onEnabledChange} />
    </div>
  </div>
);


export default ProfilePage;
