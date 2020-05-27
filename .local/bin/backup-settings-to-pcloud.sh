TARGET=~/pCloudDrive/klaasjan/backup-linux

while [ ! -d $TARGET ]
do
	sleep 20
done

mkdir -p $TARGET/local-bin
cp --archive ~/.local/bin/i3exit $TARGET/local-bin
cp --archive ~/.local/bin/i3suspend $TARGET/local-bin
cp --archive ~/.local/bin/i3display $TARGET/local-bin
cp --archive ~/.local/bin/lock $TARGET/local-bin
cp --archive ~/.local/bin/lock-multimonitor $TARGET/local-bin
cp --archive ~/.local/bin/backup-settings*.sh $TARGET/local-bin
cp --archive ~/.local/bin/reset-to-default.sh $TARGET/local-bin

cp --archive -R ~/.config/i3* $TARGET/config
cp --archive -R ~/.config/autorandr $TARGET/config
cp --archive -R ~/.config/picom $TARGET/config
cp --archive -R ~/.config/sakura $TARGET/config
mkdir -p $TARGET/home
cp --archive ~/.profile $TARGET/home
cp --archive ~/.bashrc $TARGET/home
cp --archive -R ~/.ssh $TARGET
cp --archive -R ~/Documents $TARGET
