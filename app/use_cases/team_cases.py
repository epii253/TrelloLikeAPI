from typing import Optional

from fastapi import HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth.registration import TryGetUserById
from app.crud.team.team_actions import (
    GetTeamsBoards,
    TryAddNewTeamMember,
    TryCheckUserInTeam,
    TryCreateTeam,
    TryGetTeamByName,
    TryUpdateMemberRole,
)
from app.extenshions.database.table_models.team import Role, Team, TeamMember
from app.extenshions.database.table_models.user import User
from app.schemes.responces.team_responce import (
    BoardsInfoResponceModel,
    InviteResponceModel,
    RoleUpdateResponceModel,
    TeamCreationResponceModel,
)
from app.schemes.teams_schema import InviteUserModel, NewRoleModel, NewTeamModel


async def create_team_case(
    json: NewTeamModel,
    response: Response,
    user: User,
    db: AsyncSession ,
    
) -> TeamCreationResponceModel:
    result: Optional[Team] = await TryCreateTeam(db, json, user)

    if not result:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This team-name already exists"
            )
    
    response.status_code = status.HTTP_201_CREATED
    return TeamCreationResponceModel(
                                        detail="Team created",
                                        name=result.name,
                                        owner_name=user.username,
                                        owner_id=user.id,
                                        team_id=result.id,
                                    )

async def add_member_case(
    team_name: str,
    json: InviteUserModel,
    response: Response,
    user: User,
    db: AsyncSession,
    
) -> InviteResponceModel:
    team: Optional[Team] = await TryGetTeamByName(db, team_name)
    invited_user: Optional[User] = await TryGetUserById(db, json.user_id)

    if team is None or invited_user is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="There is no such User or Team"
            )

    if team.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Only owners cand invite new users"
        )
    
    member: Optional[TeamMember] = await TryAddNewTeamMember(db, invited_user, team, Role.Worker)

    if member is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="User already in this team"
            )
    
    response.status_code = status.HTTP_201_CREATED
    return InviteResponceModel(
                                detail="User added", 
                                inviter_name=user.username, 
                                inviter_id=user.id,
                                new_member_id=invited_user.id, 
                                new_member_name=invited_user.username,
                                team_id=team.id,
                            )

async def change_role_case(
    team_name:str,
    json: NewRoleModel,
    response: Response,
    user: User,
    db: AsyncSession,
    
) -> RoleUpdateResponceModel:
    team: Optional[Team] = await TryGetTeamByName(db, team_name)
    target_user: Optional[User] = await TryGetUserById(db, json.user_id)

    if team is None or target_user is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="There is no such User or Team"
            )

    if team.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Only owners cand update roles"
        )
    
    updated_member: Optional[TeamMember] = await TryUpdateMemberRole(db, target_user, team, json.role)

    if updated_member is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Role update error"
        )
    
    response.status_code = status.HTTP_200_OK
    return RoleUpdateResponceModel(
                                    detail="role updated", 
                                    initiator=user.username, 
                                    target_id=target_user.id, 
                                    new_role=updated_member.role, 
                                    team_id=team.id,
                                )

async def get_boards_case(
    team_name: str,
    user: User,
    db: AsyncSession,

) -> BoardsInfoResponceModel:
    team: Optional[Team] = await TryGetTeamByName(db, team_name)
    
    if team is None:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Cannot find such team"
            )


    member: Optional[TeamMember] = await TryCheckUserInTeam(db, user.id, team.id)
    
    if member is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="You must be team member to get access"
            )

    return BoardsInfoResponceModel(
                                    boards = await GetTeamsBoards(db, team=team), 
                                    team=team.name, 
                                    detail=None,
                                    team_id=team.id,
                                )