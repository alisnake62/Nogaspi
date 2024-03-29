from .register import (
    CreateUserInputSchema,
    ConfirmUserCreationInputSchema,
    LoginInputSchema,
    LogoutInputSchema,
    CheckTokenValidityInputSchema
    )

from .food import (
    GetProductInputSchema,
    PostDonationFromScanInputSchema,
    PostDonationFromFridgeInputSchema,
    DeleteMyDonationsInputSchema,
    GetDonationsInputSchema,
    GetDonationByIdInputSchema,
    GetDonationsByRegularPathInputSchema,
    GetAllergensInputSchema,
    PostArticlesInFridgeInputSchema,
    DeleteArticlesInFridgeInputSchema,
    GetArticlesInFridgeInputSchema,
    TakeDonationsInputSchema,
    GenerateDonationsCodeInputSchema,
    GetFavoriteDonationsInputSchema,
    ToggleDonationInMyFavoriteInputSchema,
    GetMyDonationsInputSchema,
    RateDonationInputSchema
)
from .user import (
    GenerateRegularPathInputSchema,
    GetRegularPathInputSchema,
    PostFireBaseTokenInputSchema,
    GetMyInfosInputSchema,
    SetMyInfosInputSchema,
    PostProfilePicture,
    FilePostProfilePicture
)

from .messaging import (
    InitiateConversationInputSchema,
    PostMessageInputSchema,
    AcknowledgeMessagesOnConversationInputSchema,
    GetMyConversationsInputSchema,
    GetConversationInputSchema,
    GetConversationsByDonationInputSchema
)